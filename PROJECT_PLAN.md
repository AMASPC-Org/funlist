# FunList.ai — Project Plan

## Current Phase: Multi-Brand Scoring System (Phase 1.5)

### Development Environment
- **Primary Development**: Replit-first with PostgreSQL + Prisma
- **Architecture**: Monorepo with Central API + Brand-specific Flask apps
- **Database**: PostgreSQL (shared via Central API)
- **Deployment**: Cloud deployment deferred until Phase 3

---

## 🎯 PROJECT VISION

**FunList.ai** is evolving from a single-brand event discovery platform into a **multi-brand scoring ecosystem** supporting different event discovery experiences:

### Brand Portfolio
- **FunList** → **Funalytics™** scoring (community vibes, family-friendly focus)
- **BusinessCalendar** → **ConnectScore™** & **Elevate™** scoring (networking, professional growth)

---

## ✅ PHASE 1 COMPLETE: MVP FOUNDATION

### Core Infrastructure ✅
- Flask app scaffolding (auth, events, discovery)
- Database schema (Postgres + Prisma ORM, synced with Flask models)
- Express.js API sidecar with Prisma
- Database seeded with 25+ events and 9 users

### Event Management System ✅
- Event search + filter functionality (title, date range, location filters with validation)
- Complete CRUD operations for events
- Comprehensive input validation and error handling

### Funalytics™ AI-Powered Scoring ✅ ⭐
- **MVP Implementation Complete**: Transitioned from static fun_meter to intelligent multi-dimensional scoring
- **Database Architecture**: Append-only funalytics_scores table with complete score history
- **Smart Algorithms**: CommunityVibe & FamilyFun scoring with keyword-based intelligence
- **API Integration**: Real-time score computation in GET /events, manual recompute endpoint
- **Production-Ready Testing**: 22 integration tests with 100% pass rate

---

## 🚀 PHASE 1.5: MULTI-BRAND SCORING SYSTEM (IN PROGRESS)

### Architectural Transformation 🏗️
- **Monorepo Structure**: `/apps/central-api`, `/packages/shared-schemas`, `/apps/funlist`, `/apps/businesscalendar`
- **Generic Scoring API**: Central API serves `/scores/latest` and `/scores/compute` for multiple brands
- **Adapter Registry**: Pluggable scoring systems (Funalytics, ConnectScore, Elevate)
- **Backward Compatibility**: Legacy `/funalytics/*` routes continue working

### Multi-Brand Implementation Status
- ✅ **Monorepo Structure**: Clean separation of concerns
- ✅ **Shared Schemas**: Zod validators and TypeScript types
- ✅ **Generic Scores API**: Multi-brand endpoints operational
- ✅ **Adapter Registry**: Funalytics, ConnectScore, Elevate adapters
- ✅ **Database Schema**: Generic scores table with JSON dimensions
- 🔄 **Backward Compatibility**: Legacy routes implementation
- ⏳ **Flask App Migration**: Move to `/apps/funlist`
- ⏳ **BusinessCalendar App**: New brand implementation
- ⏳ **Integration Tests**: Multi-brand testing suite

### Success Metrics (Phase 1.5)
- Generic scoring API supporting multiple brands and systems
- Backward compatibility maintained for existing FunList functionality
- ConnectScore and Elevate algorithms operational for BusinessCalendar
- Brand-specific Flask applications consuming Central API
- Comprehensive documentation for all scoring systems

---

## 📋 PHASE 2: BRAND EXPANSION & FEATURES

### FunList Enhancements
- OpenAI API integration for advanced natural language analysis
- Enhanced community detection algorithms
- Family-friendly event recommendations

### BusinessCalendar Features
- Professional networking event scoring
- Career development opportunity detection
- Industry-specific event categorization
- LinkedIn integration for professional context

### Cross-Brand Infrastructure
- Real-time scoring updates and webhooks
- Advanced analytics dashboard
- Machine learning model training on engagement data
- A/B testing framework for scoring algorithms

---

## 📋 PHASE 3: SCALE & DEPLOY

### Deployment & Infrastructure
- Cloud deployment (GCP/Cloud Run + Cloud SQL)
- CI/CD pipeline with brand-specific deployments
- Domain setup: funlist.ai + businesscalendar.com
- Performance optimization and caching strategies

### Security & Reliability
- Security hardening across all brands
- Rate limiting and API authentication
- Monitoring and alerting systems
- Disaster recovery and backup strategies

---

## 🏗️ ARCHITECTURE DECISIONS

### Multi-Brand Design Principles
1. **Central API**: Single source of truth for scoring logic
2. **Brand Isolation**: Each brand maintains its own UI/UX identity
3. **Shared Infrastructure**: Common database and scoring algorithms
4. **Backward Compatibility**: Existing integrations continue working
5. **Extensible Design**: Easy addition of new brands and scoring systems

### Technical Stack
- **Central API**: Node.js + Express + Prisma + PostgreSQL
- **Brand Apps**: Python + Flask consuming Central API
- **Shared Schemas**: TypeScript + Zod for type safety
- **Database**: Single PostgreSQL with generic scores table

---

## 📊 CURRENT STATUS

**Multi-brand scoring system foundation is operational** with:
- ✅ **Generic Infrastructure**: Central API serving multiple brands
- ✅ **Algorithm Diversity**: 3+ scoring systems (Funalytics, ConnectScore, Elevate)
- ✅ **Data Architecture**: Generic scores table supporting all brands
- 🔄 **Integration Work**: Connecting brand-specific UIs to Central API

**Next Priority**: Complete brand-specific Flask application implementation and comprehensive testing suite.

---

**Last Updated**: September 15, 2025
**Current Focus**: Multi-brand scoring system completion and testing