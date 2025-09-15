# FunList.ai — Project Plan

## Current Phase: MVP Foundation (Phase 1)

### Development Environment
- **Primary Development**: Replit with SQLite + Prisma
- **Architecture**: Flask web app + Express.js API sidecar
- **Database**: PostgreSQL (shared between Flask and Express)
- **Deployment**: Cloud deployment deferred until Phase 3

---

### ✅ Completed
- Flask app scaffolding (authentication, events, discovery)
- Database schema implemented (Postgres + Prisma ORM synced with Flask models)
- Express.js API sidecar created with Prisma
- Integration test suite added (10 tests passing)
- Database seeded with 25+ events and 9 users

---

### 🔄 In Progress
- Event search + filter functionality
- Fun Score system (transition from static → AI-powered Funalytics)

---

### 📋 Upcoming (Phase 1)
- Finalize API endpoints (GET/POST events, users, venues)
- Expand test coverage (end-to-end: create → discover → save)
- Establish performance baselines
- Sync Replit AI prompts with PROJECT_PLAN.md & TASKS.md

---

### Future Phases

#### Phase 2: Feature Enhancement
- Digital advertising system
- Stripe integration
- Advanced search functionality
- Mobile API optimization

#### Phase 3: Scale & Deploy
- Cloud deployment (GCP/Cloud Run + SQL)
- CI/CD pipeline
- Domain setup and production environment
- Performance optimization
- Security hardening

---

### Architecture Decisions
1. **Dual Backend**: Flask for web interface, Express.js for API
2. **Shared Database**: Single PostgreSQL instance
3. **API-First**: REST endpoints for frontend + mobile integration
4. **Incremental Development**: Prioritize working flows over completeness

---

### Success Metrics (Phase 1)
- Functional event creation/discovery workflow
- API endpoints responding correctly with real DB data
- Basic user authentication working
- Database operations stable
- At least one full end-to-end flow (create → discover → save event) works without errors
- Static Fun Rating System working, Funalytics AI scoring planned

---

**Update**: Funalytics MVP implemented (API + tests). Next up: surface in Flask UI, admin action, and small hardening.