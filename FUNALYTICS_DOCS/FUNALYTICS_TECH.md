# Funalytics™ Technical Spec (MVP)

## Data Model (Prisma-style)
Historical, append-only scores per event.

```ts
model FunalyticsScore {
  id           String   @id @default(uuid())
  eventId      String
  event        Event    @relation(fields: [eventId], references: [id])

  // Facets (0–10)
  communityVibe Int?
  familyFun     Int?
  overallScore  Int?

  reasoning    String?   // short human explanation (<= 240 chars)
  computedAt   DateTime  @default(now())

  @@index([eventId, computedAt])
}
```

One Event ➜ many FunalyticsScore rows (history). Latest row by computedAt is current.

## Inputs (MVP)
- title, description
- startTime, endTime, duration
- venue.{city,state}
- simple tags (e.g., "family-friendly", "community", "music")
- organizer reputation (placeholder for later)

## Facet Rules (MVP heuristics)
- **CommunityVibe**: +2 local tags; +2 nonprofit/community keywords; +1 smaller venues; cap 10
- **FamilyFun**: +3 "family", "kid", "all ages"; −2 explicit 21+; cap 10
- **Overall**: simple average of available facets (round to nearest int)

These rules are deterministic for the MVP. Later we can move to an ML/LLM-assisted pipeline.

## Lifecycle
- **Create**: POST /events → create event → compute score → store 1 row
- **Edit**: PUT/PATCH /events/:id → recompute → append new row
- **Nightly** (later): recompute where meaningful fields changed
- **Read**: GET /events returns latest score; GET /events/:id/scores returns history (later)

## API Contract (MVP)
### GET /events
- **Query**: title, start, end, location
- **Returns**: array of events {..., funalytics: {overallScore, communityVibe, familyFun, reasoning}} (latest row only)

### POST /events
- **Body**: { title, description, startTime, endTime, organizerId, venue:{...} }
- **Behavior**: create event ➜ compute score ➜ return event + latest score

### POST /funalytics/recompute/:eventId (later in MVP)
- Recompute score for a single event; append a new history row.

## Output Example
```json
{
  "eventId": "evt_123",
  "computedAt": "2025-09-15T12:00:00Z",
  "communityVibe": 8,
  "familyFun": 9,
  "overallScore": 9,
  "reasoning": "Local vendors, kid crafts, and community music stage."
}
```

## Validation & Limits
- Facets clamped [0..10]
- Reasoning ≤ 240 chars
- If required input is missing, produce conservative defaults and a clear reasoning note.

## Versioning
- **mvp-v1** (deterministic heuristics)
- Change rules behind a feature flag; keep history rows immutable.

## Observability (later)
- Log compute latency
- Log rule hits (for debugging)