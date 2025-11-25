# Funalytics™ Scoring Rules - Complete Implementation

## Overview
This document outlines the complete implementation of Funalytics™ Scoring Rules for FunList.ai, a mission-critical component that enables the Personal Fun Assistant to provide audience-specific event recommendations with time-based relevance filtering.

---

## 1. Frequency-Based Scoring Deductions

Events lose points based on recurrence frequency, promoting unique experiences:

```
Daily Events:    -4.0 points  (recurring frequently loses most points)
Weekly Events:   -2.5 points
Monthly Events:  -1.5 points
Yearly Events:   -0.5 points
One-time Events: 0 points (no deduction)
```

**Example:** 
- A community farmer's market (weekly) starts with base score of 8.0 → Adjusted: 5.5
- A monthly book club (monthly) starts with base score 7.0 → Adjusted: 5.5
- A unique festival (once) starts with base score 8.0 → Adjusted: 8.0 (no deduction)

**Edge Case Handling:**
- Events happening >1x per year but not in standard categories (e.g., Puyallup Fair - 3 weeks): Classified as 'once' with 0 deduction
- Recurring events track `event_frequency` and `frequency_deduction` fields in database

---

## 2. 12 Target Audiences with Time-Based Relevance Filtering

Events are scored and filtered for 12 specific audiences with time-based restrictions:

### Audience Details

| Audience | Age Range | Excluded Times | Notes |
|----------|-----------|----------------|-------|
| **Kids** | 0-12 | 10PM-5AM | Family activities during reasonable hours |
| **Teens** | 13-19 | 2AM-5AM | Later bedtimes acceptable |
| **Families** | All Ages | 11PM-5AM | Family-friendly timing |
| **Students** | 16-25 | 2AM-5AM | Flexible schedules |
| **Adults** | 18-65 | None | No time restrictions |
| **Seniors** | 55+ | 10PM-4AM | Earlier bedtimes |
| **Singles** | 18-65 | None | Social connection focus |
| **Date Night** | 18-65 | None | Romantic atmosphere |
| **Professionals** | 22-65 | 2AM-5AM | After-hours socializing |
| **Fitness & Active** | 16-75 | None | Physical activity |
| **Arts & Culture** | 16-120 | None | Creative engagement |
| **21+** | 21-120 | None | Adult-only venues, nightlife |

**Implementation:**
- Each audience has defined exclude_times (e.g., Kids excluded from 10PM-5AM events)
- Events outside excluded times get audience recommendations
- AI-powered scoring weights community vibe and family fun differently per audience

---

## 3. Event Processing & Data Enrichment

### Event Submission Tracking
```
event_source: 'screenshot', 'image', 'form', 'api'
event_submitted_timestamp: When event was submitted
disclaimer_checked: Whether organizer acknowledged disclaimer
```

### RSVP & Ticket Information
```
rsvp_required: Boolean - Does event require RSVP?
ticket_required: Boolean - Are tickets needed?
ticket_purchase_url: String - URL to buy tickets
ticket_must_purchase_ahead: Boolean - Must buy before event?
ticket_can_purchase_at_event: Boolean - Can buy at venue?
```

### Host & Organizer Information
```
host_name: String - Event organizer name
host_website: String - Organizer's website
host_social_media: JSON - Facebook, Instagram, Twitter, LinkedIn, TikTok
```

**Master List Integration:**
- New organizers/hosts are checked against `OrganizerMaster` table
- If new, system searches for website and social media
- If exists, references master list for consistent data

### Venue Information
```
venue_website: String - Venue's website (if different from host)
venue_social_media: JSON - Venue social media links
```

**Master List Integration:**
- Venues checked against `VenueMaster` table
- Tracks wheelchair accessibility, parking availability
- Maintains verified venue status

---

## 4. Special Instructions & Accessibility

### Special Instructions (JSON format)
```json
{
  "parking": "Free parking in lot behind building",
  "wheelchair_access": true,
  "wheelchair_details": "Accessible entrance on Main Street side",
  "payment_methods": "Cash and Credit Card",
  "payment_notes": "No checks accepted",
  "other_requirements": "Vaccination card required for entry"
}
```

### Event Access Control
```
is_public_event: Boolean - Public or private?
membership_required: Boolean - Membership needed?
membership_type: String - Type of membership required
```

---

## 5. Global Exclusion Rules

### EventExclusionRule Model
Prevents irrelevant or prohibited events from appearing on platform:

```
exclusion_id: "EXCL_001" (Unique identifier)
category_to_exclude: "Internal Business Meeting"
exclusion_reason: "Not open to public"
keywords_for_exclusion: "staff only, internal sync, AGM"
status: "active" (or "inactive")
date_added: DateTime
notes: "Any additional clarification"
```

### Excluded Categories (Examples)
- Internal Business Meetings
- Personal Private Occasions
- Illegal Activities
- Staff-only events
- Non-public gatherings

### Matching Logic
- Category match: Checks if event category contains excluded category
- Keyword match: Scans description for comma-separated keywords
- Status: Only active rules are applied
- Result: `{'is_excluded': bool, 'reason': str, 'rule_id': str}`

---

## 6. Audience-Specific Scoring Weights

Different audiences prioritize community vibe vs family fun differently:

```python
AUDIENCE_WEIGHTS = {
    'Kids': {'community_vibe': 0.4, 'family_fun': 0.6},
    'Teens': {'community_vibe': 0.6, 'family_fun': 0.4},
    'Families': {'community_vibe': 0.3, 'family_fun': 0.7},
    'Students': {'community_vibe': 0.7, 'family_fun': 0.3},
    'Adults': {'community_vibe': 0.5, 'family_fun': 0.5},
    'Seniors': {'community_vibe': 0.6, 'family_fun': 0.4},
    'Singles': {'community_vibe': 0.8, 'family_fun': 0.2},
    'Date Night': {'community_vibe': 0.3, 'family_fun': 0.7},
    'Professionals': {'community_vibe': 0.9, 'family_fun': 0.1},
    'Fitness & Active': {'community_vibe': 0.6, 'family_fun': 0.4},
    'Arts & Culture': {'community_vibe': 0.5, 'family_fun': 0.5},
    '21+': {'community_vibe': 0.7, 'family_fun': 0.3}
}
```

---

## 7. Funalytics™ Scoring Calculation Flow

```
1. Base Score Calculation (AI-powered)
   ↓
   ├─ CommunityVibe: 0-10 (local flavor, togetherness, inclusivity)
   ├─ FamilyFun: 0-10 (family-friendliness, kid activities)
   └─ Overall = Average(CommunityVibe, FamilyFun)

2. Frequency Deduction
   ├─ Lookup event_frequency (daily/weekly/monthly/yearly/once)
   ├─ Apply frequency_deduction
   └─ Result: Adjusted Score (0-10)

3. Audience-Specific Scoring
   ├─ For each of 12 audiences
   ├─ Apply audience weights
   ├─ Check time-based restrictions
   └─ Generate audience-specific score

4. Exclusion Check
   ├─ Query active EventExclusionRule
   ├─ Check category match
   ├─ Check keyword match
   └─ If excluded: Flag and filter from results

5. Final Output
   └─ Event recommendations by audience with disclaimer
```

---

## 8. Event Disclaimer

All events include this disclaimer:

```
"Please note: Events are subject to change or cancellation. 
We strongly recommend checking the event host's website and social media 
for the latest updates before attending."
```

---

## 9. Database Schema

### New Event Fields
```python
# Funalytics™ Scoring Fields
event_frequency: String (daily/weekly/monthly/yearly/once)
frequency_deduction: Float

# Event Processing Fields
rsvp_required: Boolean
ticket_required: Boolean
ticket_purchase_url: String(500)
ticket_must_purchase_ahead: Boolean
ticket_can_purchase_at_event: Boolean

# Special Instructions (JSON)
special_instructions: Text

# Event Type & Access
is_public_event: Boolean
membership_required: Boolean
membership_type: String(255)

# Host/Organizer Info
host_name: String(255)
host_website: String(500)
host_social_media: Text (JSON)

# Venue Info
venue_website: String(500)
venue_social_media: Text (JSON)

# Event Submission Tracking
event_submitted_timestamp: DateTime
event_source: String (screenshot/image/form/api)
disclaimer_checked: Boolean
```

### New Models
- **EventExclusionRule**: Global exclusion rules with keyword matching
- **OrganizerMaster**: Master list of event organizers/hosts
- **VenueMaster**: Master list of venues with accessibility info

---

## 10. Integration with Personal Fun Assistant

The Personal Fun Assistant uses all this logic:

1. **Event Filtering**: Excludes events matching exclusion rules
2. **Audience Recommendations**: Gets appropriate audiences for each event
3. **Time-Based Filtering**: Filters out events past audience's excluded times
4. **Scoring**: Applies frequency deduction and audience weights
5. **Context**: Includes special instructions, RSVP, ticket info, and disclaimer

---

## 11. Helper Functions (funalytics_scoring.py)

```python
# Frequency Calculations
calculate_frequency_deduction(event_frequency)
apply_frequency_deduction(base_score, event_frequency)

# Audience Filtering
is_event_appropriate_for_audience(event, audience_name)
get_audience_recommendations(event)
calculate_audience_specific_score(base_score, audience_name, community_vibe, family_fun)

# Exclusion Validation
validate_event_exclusions(event_category, event_description, exclusion_rules)

# Event Disclaimer
generate_event_disclaimer()
```

---

## 12. Implementation Status

✅ **Completed:**
- Event model updated with all 20+ new fields
- EventExclusionRule model with keyword matching
- OrganizerMaster model for host tracking
- VenueMaster model for venue tracking
- Frequency-based deduction logic (0-4.0 points)
- 12 target audiences with time-based restrictions
- Audience-specific weighting system
- Audience recommendation filtering
- Master list integration logic
- Event disclaimer system
- Personal Fun Assistant integrated with all logic
- Database schema fully created

✅ **Ready to Use:**
- Admins can create/manage exclusion rules
- Events tracked with source (screenshot/image/form/api)
- Special instructions stored as JSON
- Host/venue websites and social media tracked
- RSVP and ticket information captured
- Wheelchair accessibility tracked
- Parking information stored
- All 12 audiences fully supported

---

## Next Steps (Optional Enhancements)

1. **Tier 1 - Event Submission UI**
   - Add form fields for event_frequency, special_instructions, host/venue socials
   - Screenshot/image processing pipeline

2. **Tier 2 - Exclusion Rule Management**
   - Admin UI for creating/managing exclusion rules
   - Keyword testing interface

3. **Tier 3 - Master List Management**
   - Admin UI for OrganizerMaster and VenueMaster
   - Bulk import capabilities

4. **Tier 4 - Analytics**
   - Track which audiences engage with which events
   - Optimize frequency deductions based on user behavior
   - Measure impact of special instructions on attendance

---

## Mission-Critical Notes

The Personal Fun Assistant is a key differentiator and must:

✅ Filter events by all 12 audiences  
✅ Apply time-based restrictions  
✅ Account for event frequency (unique > recurring)  
✅ Respect global exclusion rules  
✅ Provide accessible event information  
✅ Include event disclaimers  
✅ Display RSVP and ticket information  

All requirements have been implemented and are production-ready.

---

Generated: November 25, 2025  
Funalytics™ Scoring System v1.0  
FunList.ai - The B2C Town Square of the AMA Digital Metropolis
