# Multi-Brand Scoring Systems Overview

## 🎯 Vision

FunList.ai has evolved into a **multi-brand scoring ecosystem** that powers different event discovery experiences through specialized scoring algorithms tailored to distinct audiences and use cases.

## 🏢 Brand Portfolio

### FunList → Funalytics™
**Target Audience**: Families, community enthusiasts, casual event-goers
**Focus**: Community engagement, family-friendly experiences, local connections

**Scoring Dimensions**:
- **CommunityVibe™** (0-10): Sense of togetherness, local flavor, inclusivity
- **FamilyFun™** (0-10): Suitability for families and children
- **Overall Score**: Balanced composite reflecting entertainment value

**Use Cases**:
- Family weekend planning
- Community event discovery  
- Local business promotion
- Neighborhood engagement

[**📖 Full Documentation**: docs/FUNALYTICS_DOCS](./FUNALYTICS_DOCS.md)

---

### BusinessCalendar → ConnectScore™ & Elevate™

**Target Audience**: Professionals, entrepreneurs, business networks, career-focused individuals
**Focus**: Professional growth, networking opportunities, skill development

#### ConnectScore™
**Purpose**: Networking potential and professional relationship building

**Scoring Dimensions**:
- **NetworkingPotential** (0-10): Quality of professional connections available
- **IndustryRelevance** (0-10): Alignment with current professional trends
- **CareerImpact** (0-10): Potential for career advancement or development

#### Elevate™
**Purpose**: Personal and professional development opportunities

**Scoring Dimensions**:
- **SkillBuilding** (0-10): Learning opportunities and skill enhancement
- **LeadershipExposure** (0-10): Access to thought leaders and mentors
- **GrowthPotential** (0-10): Long-term professional development value

**Use Cases**:
- Professional conference selection
- Industry networking events
- Skill development workshops
- Executive education programs

[**📖 ConnectScore Documentation**: docs/CONNECT_SCORE_DOCS](./CONNECT_SCORE_DOCS.md)

---

## 🏗️ Technical Architecture

### Central Scoring API
All scoring systems are powered by a unified **Central API** that provides:

- **Generic Endpoints**: `/scores/latest` and `/scores/compute` supporting all brands
- **Adapter Registry**: Pluggable scoring algorithms for easy extension
- **Shared Database**: Generic scores table with JSON dimensions for flexibility
- **Backward Compatibility**: Legacy API routes continue working seamlessly

### Multi-Brand Data Model

```typescript
interface Score {
  id: string;
  brand: 'funlist' | 'businesscalendar';
  system: 'Funalytics' | 'ConnectScore' | 'Elevate';
  entityType: 'event' | 'venue' | 'experience';
  entityId: number;
  overallScore: number;
  dimensions: Record<string, number>; // Flexible JSON structure
  reasoning: string;
  computedAt: Date;
}
```

### Algorithm Adapters

Each scoring system implements a common interface:

```typescript
interface ScoringAdapter {
  computeScore(params: {
    entityType: string;
    entity: EntityData;
  }): Promise<{
    overallScore: number;
    dimensions: Record<string, number>;
    reasoning: string;
    status: 'completed' | 'failed';
  }>;
}
```

## 🔄 API Integration

### Generic Multi-Brand API

```bash
# Get latest scores for any brand/system
GET /scores/latest?brand=funlist&system=Funalytics&entityType=event

# Compute new scores
POST /scores/compute
{
  "brand": "businesscalendar",
  "system": "ConnectScore", 
  "entityType": "event",
  "entityId": 123
}
```

### Backward Compatibility

```bash
# Legacy FunList API continues working
GET /funalytics/latest?entityType=event&entityId=123
POST /funalytics/compute
{
  "entityType": "event",
  "entityId": 123
}
```

## 📊 Scoring Algorithm Summary

| Brand | System | Primary Focus | Key Dimensions | Target Score Range |
|-------|--------|---------------|----------------|-------------------|
| FunList | Funalytics™ | Family/Community Fun | CommunityVibe, FamilyFun | 0-10 (higher = more fun) |
| BusinessCalendar | ConnectScore™ | Professional Networking | NetworkingPotential, IndustryRelevance, CareerImpact | 0-10 (higher = better networking) |
| BusinessCalendar | Elevate™ | Career Development | SkillBuilding, LeadershipExposure, GrowthPotential | 0-10 (higher = more growth) |

## 🚀 Benefits of Multi-Brand Architecture

### For Users
- **Specialized Experiences**: Scoring tailored to specific needs and contexts
- **Cross-Brand Discovery**: Professional users can still access family events when needed
- **Improved Relevance**: Algorithms optimized for distinct user personas

### For Platform
- **Scalable Design**: Easy addition of new brands and scoring systems
- **Shared Infrastructure**: Reduced development and maintenance overhead
- **Unified Analytics**: Cross-brand insights and trend analysis
- **Backward Compatibility**: Smooth transition from single-brand system

## 🔮 Future Expansion

The multi-brand architecture enables easy addition of new scoring systems:

- **WellnessCalendar** → **HealthScore™** (fitness events, wellness workshops)
- **CreativeEvents** → **InspirationMeter™** (artistic events, creative workshops)  
- **TechEvents** → **InnovationIndex™** (tech conferences, startup events)

---

**Architecture**: Monorepo with Central API + Brand-specific Applications
**Database**: Single PostgreSQL with generic scores table
**API**: RESTful endpoints with Zod validation and TypeScript types
**Documentation**: Comprehensive guides for each scoring system

**Last Updated**: September 15, 2025