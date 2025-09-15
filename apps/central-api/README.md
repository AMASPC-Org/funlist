# FunList Express.js API

A minimal Express.js API layer with Prisma ORM for the FunList.ai event discovery platform.

## Setup

The API is configured to work alongside your existing Flask application, running on port 3001.

### Dependencies
- Express.js 4.18.2
- Prisma 5.7.1
- @prisma/client 5.7.1
- dotenv 16.3.1

### Environment Variables
```
DATABASE_URL=postgresql://...
PORT=3001
NODE_ENV=development
```

## API Endpoints

### Health Check
**GET /health**
```bash
curl http://localhost:3001/health
```
Response:
```json
{
  "status": "OK",
  "message": "FunList API is running",
  "timestamp": "2025-09-15T14:23:29.296Z",
  "port": 3001
}
```

### Get Events
**GET /events**
```bash
curl http://localhost:3001/events
```
Response:
```json
{
  "success": true,
  "count": 1,
  "events": [
    {
      "id": 1,
      "title": "Sample Community Event",
      "description": "A great community gathering",
      "startTime": "2025-09-20T18:00:00.000Z",
      "endTime": "2025-09-20T21:00:00.000Z",
      "location": "Community Center",
      "city": "Seattle",
      "state": "WA",
      "category": "Community",
      "funalyticsScore": {
        "fun_rating": 4,
        "fun_meter": 4
      },
      "organizer": {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "company_name": "Community Events Inc",
        "email": "john@example.com"
      },
      "venue": {
        "id": 1,
        "name": "Downtown Community Center",
        "street": "123 Main St",
        "city": "Seattle",
        "state": "WA",
        "zip_code": "98101",
        "venue_type": {
          "name": "Community Center",
          "category": "Public"
        }
      },
      "status": "approved",
      "created_at": "2025-09-15T14:23:29.296Z"
    }
  ]
}
```

### Create Event
**POST /events**
```bash
curl -X POST http://localhost:3001/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Event",
    "description": "A test event",
    "startTime": "2025-10-15T19:00:00Z",
    "endTime": "2025-10-15T22:00:00Z",
    "organizerId": "1",
    "venue": {
      "name": "Test Venue",
      "city": "Seattle",
      "state": "WA"
    }
  }'
```

**Required Fields:**
- `title` (string): Event title
- `startTime` (ISO 8601 date): Event start time
- `organizerId` (string/number): ID of the organizer

**Optional Fields:**
- `description` (string): Event description
- `endTime` (ISO 8601 date): Event end time
- `venue` (object): Venue information

**Validation Rules:**
- Title cannot be empty
- Start time must be before end time (if both provided)
- Organizer ID is required

Success Response (201):
```json
{
  "success": true,
  "message": "Event created successfully",
  "event": {
    "id": 1757946210625,
    "title": "Test Event",
    "description": "A test event",
    "startTime": "2025-10-15T19:00:00.000Z",
    "endTime": "2025-10-15T22:00:00.000Z",
    "organizer": {
      "id": 1,
      "first_name": "Mock",
      "last_name": "Organizer",
      "company_name": "Event Company",
      "email": "organizer@example.com"
    },
    "venue": {
      "name": "Test Venue",
      "city": "Seattle",
      "state": "WA"
    },
    "status": "pending",
    "created_at": "2025-09-15T14:23:30.625Z"
  }
}
```

Validation Error Response (400):
```json
{
  "success": false,
  "error": "Validation failed",
  "details": [
    "Title is required",
    "Start time must be before end time",
    "Organizer ID is required"
  ]
}
```

## Running the API

The API is configured as a workflow and runs automatically. To start manually:

```bash
cd api
node run.js
```

## CORS Configuration

The API includes CORS headers to allow requests from your Flask application and other origins.

## Next Steps

1. **Database Connection**: Once Flask migrations are complete, the API will connect to the real database
2. **Authentication**: Add JWT or session-based authentication
3. **Rate Limiting**: Implement request rate limiting
4. **Additional Endpoints**: Add PUT/DELETE operations for events
5. **Pagination**: Add proper pagination with limit/offset parameters
6. **Filtering**: Add query parameters for filtering events by date, location, category, etc.

## Architecture

This API runs as a separate service alongside your Flask application:
- Flask App: Port 8080 (web interface)
- Express API: Port 3001 (JSON API)
- Database: Shared PostgreSQL database

The separation allows for:
- Independent scaling of web interface vs API
- Different technology stacks for different use cases
- API-first development for mobile apps or external integrations