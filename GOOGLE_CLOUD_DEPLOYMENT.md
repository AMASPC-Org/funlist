# Google Cloud Deployment Guide for FunList.ai

## Overview
This guide provides comprehensive instructions for deploying the FunList.ai Flask application to Google Cloud Run via GitHub integration. The application uses Flask with PostgreSQL (Cloud SQL) for the database and database-backed sessions for scalability.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Google Cloud Setup](#google-cloud-setup)
3. [Cloud SQL Configuration](#cloud-sql-configuration)
4. [Environment Variables](#environment-variables)
5. [GitHub Integration](#github-integration)
6. [Deployment Process](#deployment-process)
7. [Post-Deployment Verification](#post-deployment-verification)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Google Cloud Services
- Google Cloud Project with billing enabled
- Cloud Run API enabled
- Cloud SQL Admin API enabled
- Cloud Build API enabled
- Container Registry API enabled
- Secret Manager API enabled (for storing sensitive environment variables)

### Required API Keys and Credentials
- Google Maps API key
- At least one AI service API key (Anthropic, OpenAI, or Google Gemini)
- Firebase project (with Google sign-in enabled), web client config, and a service account key for the same project (used by the backend to verify Firebase ID tokens)

### Local Development Tools
- Google Cloud SDK (`gcloud` CLI)
- Docker (for local testing)
- Git

## Google Cloud Setup

### 1. Enable Required APIs
```bash
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### 2. Create Service Account
```bash
# Create service account for Cloud Run
gcloud iam service-accounts create funlist-app-sa \
    --display-name="FunList App Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:funlist-app-sa@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client"

gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:funlist-app-sa@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

## Cloud SQL Configuration

### 1. Create Cloud SQL Instance
```bash
gcloud sql instances create funlist-db \
    --database-version=POSTGRES_14 \
    --tier=db-f1-micro \
    --region=us-central1 \
    --network=default \
    --no-backup
```

### 2. Create Database
```bash
gcloud sql databases create funlist \
    --instance=funlist-db
```

### 3. Set Database Password
```bash
gcloud sql users set-password postgres \
    --instance=funlist-db \
    --password=YOUR_SECURE_PASSWORD
```

### 4. Get Connection String
Your Cloud SQL connection string format:
```
postgresql://postgres:PASSWORD@/funlist?host=/cloudsql/PROJECT_ID:us-central1:funlist-db
```

## Environment Variables

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_SECRET_KEY` | **REQUIRED** - Secret key for Flask sessions (min 32 chars) | Generate with: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DATABASE_URL` | **REQUIRED** - PostgreSQL connection string | `postgresql://postgres:password@/funlist?host=/cloudsql/PROJECT:REGION:INSTANCE` |
| `GOOGLE_MAPS_API_KEY` | **REQUIRED** - Google Maps API key for location services | Your Google Maps API key |
| `FLASK_ENV` | Flask environment | `production` |
| `PORT` | Application port | `8080` |

### Optional Environment Variables

| Variable | Description | Required For |
|----------|-------------|--------------|
| `FIREBASE_ENABLED` | Toggle Firebase auth integration | Google sign-in via Firebase |
| `FIREBASE_PROJECT_ID` | Firebase project ID | Google sign-in via Firebase |
| `FIREBASE_API_KEY` | Firebase web API key | Google sign-in via Firebase |
| `FIREBASE_AUTH_DOMAIN` | Firebase auth domain | Google sign-in via Firebase |
| `FIREBASE_STORAGE_BUCKET` | Firebase storage bucket | Google sign-in via Firebase |
| `FIREBASE_MESSAGING_SENDER_ID` | Firebase messaging sender ID | Google sign-in via Firebase |
| `FIREBASE_APP_ID` | Firebase app ID | Google sign-in via Firebase |
| `FIREBASE_CREDENTIALS_JSON` | Service account JSON (or set `FIREBASE_CREDENTIALS_PATH`) | Google sign-in via Firebase |
| `ANTHROPIC_API_KEY` | Anthropic Claude API key | AI Fun Assistant |
| `OPENAI_API_KEY` | OpenAI GPT API key | AI Fun Assistant |
| `GEMINI_API_KEY` | Google Gemini API key | AI Fun Assistant |
| `EXPRESS_API_URL` | Express API backend URL | Funalytics features |

### Setting Environment Variables in Cloud Run

#### Using Secret Manager (Recommended for sensitive data)
```bash
# Create secrets
echo -n "your-secret-key" | gcloud secrets create flask-secret-key --data-file=-
echo -n "your-db-url" | gcloud secrets create database-url --data-file=-
echo -n "your-maps-key" | gcloud secrets create google-maps-api-key --data-file=-

# Grant access to service account
gcloud secrets add-iam-policy-binding flask-secret-key \
    --member="serviceAccount:funlist-app-sa@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

## GitHub Integration

### 1. Connect GitHub Repository
1. Go to Cloud Build in Google Cloud Console
2. Navigate to "Triggers"
3. Click "Connect Repository"
4. Choose GitHub and authenticate
5. Select your repository
6. Grant necessary permissions

### 2. Create Build Trigger
```bash
gcloud builds triggers create github \
    --repo-name=your-repo-name \
    --repo-owner=your-github-username \
    --branch-pattern="^main$" \
    --build-config=cloudbuild.yaml \
    --substitutions="_REGION=us-central1,_SERVICE_NAME=funlist-app"
```

### 3. Configure Build Substitutions
Add these substitution variables in Cloud Build trigger settings:
- `_REGION`: Deployment region (e.g., `us-central1`)
- `_SERVICE_NAME`: Cloud Run service name (e.g., `funlist-app`)
- `_MIN_INSTANCES`: Minimum instances (e.g., `1`)
- `_MAX_INSTANCES`: Maximum instances (e.g., `100`)
- `_MEMORY`: Memory allocation (e.g., `1Gi`)
- `_CPU`: CPU allocation (e.g., `1`)

## Deployment Process

### Automatic Deployment (via GitHub)
1. Push code to main branch:
   ```bash
   git add .
   git commit -m "Deploy to Cloud Run"
   git push origin main
   ```

2. Cloud Build automatically:
   - Builds Docker image
   - Pushes to Container Registry
   - Deploys to Cloud Run

### Manual Deployment
```bash
# Build and push image
docker build -t gcr.io/PROJECT_ID/funlist-app .
docker push gcr.io/PROJECT_ID/funlist-app

# Deploy to Cloud Run
gcloud run deploy funlist-app \
    --image=gcr.io/PROJECT_ID/funlist-app \
    --region=us-central1 \
    --platform=managed \
    --allow-unauthenticated \
    --set-env-vars="FLASK_ENV=production,PORT=8080" \
    --set-secrets="FLASK_SECRET_KEY=flask-secret-key:latest,DATABASE_URL=database-url:latest" \
    --add-cloudsql-instances=PROJECT_ID:us-central1:funlist-db \
    --service-account=funlist-app-sa@PROJECT_ID.iam.gserviceaccount.com
```

## Post-Deployment Verification

### 1. Check Service Status
```bash
gcloud run services describe funlist-app --region=us-central1
```

### 2. Test Health Endpoint
```bash
# Get service URL
SERVICE_URL=$(gcloud run services describe funlist-app --region=us-central1 --format='value(status.url)')

# Test health check
curl $SERVICE_URL/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00",
  "service": "funlist-app",
  "checks": {
    "application": "ok",
    "database": "ok"
  }
}
```

### 3. Verify Database Connection
Check Cloud Run logs for database connection status:
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=funlist-app" --limit=50
```

### 4. Test Session Persistence
1. Access the application
2. Log in or perform actions that create session data
3. Verify sessions are stored in `flask_sessions` table:
   ```sql
   SELECT COUNT(*) FROM flask_sessions;
   ```

## Monitoring and Maintenance

### Cloud Run Metrics
Monitor in Google Cloud Console:
- Request count and latency
- Instance count and CPU/memory usage
- Error rate
- Cold start frequency

### Database Monitoring
- Connection pool usage
- Query performance
- Storage usage
- Backup status

### Logging
View logs:
```bash
# Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision" --limit=50

# Cloud SQL logs
gcloud logging read "resource.type=cloudsql_database" --limit=50
```

### Scaling Configuration
Adjust based on traffic patterns:
```bash
gcloud run services update funlist-app \
    --min-instances=2 \
    --max-instances=200 \
    --concurrency=100
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Errors
**Error**: "could not connect to server: No such file or directory"
**Solution**: 
- Verify Cloud SQL instance is running
- Check connection string format
- Ensure Cloud SQL Admin API is enabled
- Verify service account has `cloudsql.client` role

#### 2. Session Storage Issues
**Error**: "relation 'flask_sessions' does not exist"
**Solution**:
- SSH into a Cloud Run instance or use Cloud SQL proxy
- Manually create the sessions table if needed
- Verify Flask-Session is properly initialized

#### 3. Environment Variable Issues
**Error**: "FLASK_SECRET_KEY environment variable must be set"
**Solution**:
- Verify all required environment variables are set in Cloud Run
- Check Secret Manager permissions
- Use `gcloud run services describe` to view current configuration

#### 4. Memory/Timeout Issues
**Error**: "The request was aborted because the worker process..."
**Solution**:
```bash
gcloud run services update funlist-app \
    --memory=2Gi \
    --timeout=900 \
    --cpu=2
```

#### 5. HTTPS/Security Issues
**Error**: Mixed content or cookie security warnings
**Solution**:
- Ensure all resources use HTTPS
- Verify CSP headers are correctly configured
- Check SESSION_COOKIE_SECURE is True

### Debug Commands

```bash
# View service configuration
gcloud run services describe funlist-app --region=us-central1

# View recent logs
gcloud logging read "resource.type=cloud_run_revision AND severity>=ERROR" --limit=20

# Test database connection locally
gcloud sql proxy PROJECT_ID:us-central1:funlist-db &
psql "host=127.0.0.1 port=5432 dbname=funlist user=postgres"

# View Cloud Build history
gcloud builds list --limit=5

# Check service permissions
gcloud run services get-iam-policy funlist-app --region=us-central1
```

## Security Best Practices

1. **Secret Management**
   - Never hardcode secrets in code
   - Use Secret Manager for all sensitive data
   - Rotate secrets regularly

2. **Database Security**
   - Use Cloud SQL private IP when possible
   - Enable SSL/TLS for database connections
   - Implement least privilege access

3. **Application Security**
   - Keep FLASK_SECRET_KEY secure and unique
   - Ensure SESSION_COOKIE_SECURE is True
   - Implement rate limiting
   - Regular dependency updates

4. **Network Security**
   - Use VPC connector for private resources
   - Implement Cloud Armor for DDoS protection
   - Configure appropriate CORS policies

## Cost Optimization

1. **Cloud Run**
   - Set appropriate min/max instances
   - Optimize cold start performance
   - Use concurrency settings effectively

2. **Cloud SQL**
   - Use appropriate instance size
   - Enable automatic backups only if needed
   - Consider read replicas for high traffic

3. **Monitoring**
   - Set up budget alerts
   - Review and optimize unused resources
   - Use committed use discounts for predictable workloads

## Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Flask-Session Documentation](https://flask-session.readthedocs.io/)
- [Google Cloud Security Best Practices](https://cloud.google.com/security/best-practices)

## Support

For deployment issues:
1. Check Cloud Run logs and Cloud Build history
2. Verify all environment variables are set
3. Ensure database connectivity
4. Review this guide's troubleshooting section

For application issues:
1. Check application logs in Cloud Logging
2. Verify health endpoint: `/health`
3. Test database connection
4. Review session storage in flask_sessions table
