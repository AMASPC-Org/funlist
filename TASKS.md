# FunList.ai — Active Task Backlog (Replit Focused)

This file is the working backlog for Replit AI.  
It contains only the tasks needed to build and test the MVP inside Replit.  
Cloud infra and deployment steps will be reintroduced later.

---

## ✅ Completed
- Repo created in GitHub  
- Replit project connected  
- Database schema (schema.sql) committed  
- Project plan documented (PROJECT_PLAN.md)  

---

## 🚧 Phase 1: MVP Foundation (Replit Dev Only)

### 1. Database & Backend (local Prisma + SQLite in Replit)
- [ ] Configure Prisma ORM to use SQLite for local dev.  
- [ ] Implement User, Event, Venue, Favorite models (match schema.sql).  
- [ ] Add seed script with sample users, events, venues.  
- [ ] Expose REST endpoints for:  
  - User registration/login (attendee, organizer, admin).  
  - Event submission (organizer).  
  - Event search + filter (date/location).  
  - Favorites (attendees save events).  

### 2. Core Features
- [ ] Event submission form (organizer).  
- [ ] Event discovery UI (attendee list + search).  
- [ ] Personal Fun Assistant (chat UI stub with mock data).  
- [ ] Display Fun Ratings (static values for now).  

### 3. Testing
- [ ] Add integration tests for user login + event submission.  
- [ ] Add sample test for Fun Assistant chat flow.  

---

## 📌 Notes
- Replit AI: Use **SQLite** in dev (`file:./dev.db`) to avoid Cloud SQL setup.  
- Schema and ORM must stay aligned (see schema.sql and prisma/schema.prisma).  
- Commit code in small steps so features can be tested incrementally.  

---