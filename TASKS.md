# FunList.ai — Active Task Backlog

This file tracks all outstanding tasks in a lightweight, developer-friendly format.  
Each item should be updated with status markers:  
- [ ] = not started  
- [~] = in progress  
- [x] = completed  

---

## ✅ Completed
- [x] Repo created in GitHub
- [x] Replit project connected
- [x] schema.sql committed

---

## 🚧 Phase One: MVP Foundation

### Database
- [ ] Apply schema.sql to Postgres instance in GCP
- [ ] Set up migrations framework (Prisma / Alembic / Flyway)
- [ ] Create ORM models based on schema
- [ ] Seed DB with sample users, venues, and events

### Backend
- [ ] Implement user registration & login (attendee, organizer, admin)
- [ ] Implement organizer event submission endpoint
- [ ] Implement event search & filter (location/date)
- [ ] Implement Funalytics scoring endpoint
- [ ] Implement favorites (attendees can save events)

### Infrastructure
- [ ] Deploy backend to Cloud Run
- [ ] Add CI/CD pipeline via Cloud Build
- [ ] Configure monitoring & logging
- [ ] Add health checks

---

## 🚧 Phase Two: Event Attendee Experience
- [ ] Build Personal Fun Assistant (attendee-facing AI chatbot)
- [ ] Integrate Funalytics scoring into chatbot flow
- [ ] Create responsive event listing & detail pages
- [ ] Implement organizer dashboard
- [ ] Add map-based event discovery

---

## 🚧 Phase Three: Organizers & Ecosystem
- [ ] Add AI-powered event optimization suggestions
- [ ] Build analytics dashboard for organizers
- [ ] Support multi-user organization accounts
- [ ] Explore LocalMarketingTool.ai integration
- [ ] Explore AMA SPC ecosystem integration

---

## 📌 Notes
- Keep this backlog in sync with real progress.  
- Treat this like a lightweight sprint board.  
- Update statuses often so Replit AI and contributors can stay aligned.
