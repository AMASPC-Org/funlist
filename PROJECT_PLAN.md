# FunList.ai — Project Roadmap & Execution Plan

_Last updated: 2025-09-15_

---

## 🎯 Purpose
This file is a **living roadmap** for FunList.ai.  
It ensures Replit AI and all developers have a consistent, clear project direction.  
Cloud deployment tasks are deferred until the MVP is validated in Replit.

---

## ✅ Completed
- Initial repo setup in GitHub  
- Replit project connected  
- Database schema (schema.sql) committed  
- Active backlog created (TASKS.md)  

---

## 🚧 Phase One: MVP (Replit Development Only)

1. **Database & Backend**
   - Configure Prisma ORM with SQLite (`file:./dev.db`)  
   - Implement models for Users, Events, Venues, Favorites  
   - Add seed script with sample users, venues, and events  
   - Build REST API endpoints for:  
     - User registration & login (attendee, organizer, admin)  
     - Organizer event submission  
     - Event search & filter (date/location)  
     - Attendee favorites  

2. **Core Features**
   - Organizer event submission form (frontend)  
   - Attendee event discovery UI (list + search)  
   - **Personal Fun Assistant (stub)** — chat UI returning mock responses  
   - Display Fun Ratings (static placeholders for now)  

3. **Testing**
   - Integration tests for login + event submission  
   - Basic test for Fun Assistant chat flow  

---

## 🔮 Future Phases (Parked for Now)
These will come after MVP validation in Replit:  
- Switch SQLite → Cloud SQL (Postgres on GCP)  
- CI/CD pipeline with Cloud Build + Cloud Run  
- TLS + domain setup for funlist.ai  
- Funalytics™ scoring (CommunityVibe™, FamilyFun™, Overall)  
- Organizer AI Assistant (pre-publish coaching)  
- Event ingestion agents (scrapers, email parsers)  

---

## 📌 Notes
- Replit AI should always reference this file and `TASKS.md` before writing code.  
- The immediate focus is **MVP core flows in Replit only**.  
- Cloud infra is explicitly deferred until the core experience is working.  

---
