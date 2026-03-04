# AMA Cloud Native Standards 2026

## 1. Core Stack

- **Node.js/TypeScript**: Strict mode enabled (`"strict": true`, `"noImplicitAny": true`).
- **Next.js**: The single source of truth for the frontend architecture.
- **No Vite / No Tailwind**: Use vanilla CSS or SCSS. Tailwind CSS is strictly forbidden in this ecosystem, as per the audit. We use tailored CSS for premium PNW professional markets.
- **Database**: Migration from Drizzle (PostgreSQL) to Firestore NoSQL (`@google-cloud/firestore`).

## 2. AI & Infrastructure

- **Vertex AI SDK**: All AI calls must use `@google-cloud/vertexai`. Do not use `@google/generative-ai` consumer SDKs.
- **Authentication**: Native GCP Application Default Credentials (ADC) must be used. Never use hardcoded API keys or `GEMINI_API_KEY`.
- **Model Standard**: Use `gemini-3.1-pro` model alias for zero-maintenance upgrades.
- **A2A Mesh**: All AI Microservices must expose `/.well-known/agent.json` (Agent Card) via Google ADK standard.

## 3. Data Contracts

- **Spatial Data**: All backend API responses for events/venues must explicitly map and return `latitude` and `longitude` fields for Google Maps Geometry integration.
- **Dual-Write Pipelines**: Support writing to both PostgreSQL and Firestore during the Strangler Fig DB migration. Target state is Firestore with collections: `staging_drafts`, `production_events`, `venues`, and `organizations`.

## 4. Code Hygiene

- Do not tolerate `any` casting.
- Clean npm workspace management required. Do not manually copy `node_modules` between apps.
