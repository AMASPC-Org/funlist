#!/bin/bash
set -e

SERVICE_NAME="funlist-ui"
REGION="us-west1"
PROJECT_ID="$(gcloud config get-value project 2>/dev/null)"
IMAGE_NAME="gcr.io/${PROJECT_ID:-your-gcp-project}/${SERVICE_NAME}:latest"

echo "Building the Docker image..."
gcloud builds submit . --tag "$IMAGE_NAME"

echo "Deploying the image to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
  --image "$IMAGE_NAME" \
  --region "$REGION" \
  --allow-unauthenticated \
  --min-instances=0 \
  --max-instances=20

echo "Deployment successful!"
