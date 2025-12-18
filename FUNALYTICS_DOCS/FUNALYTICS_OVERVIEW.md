# Funalytics™ Overview

## What it is
Funalytics™ is FunList.ai's scoring & explanation system that helps people quickly gauge how enjoyable an event might be. It produces human-readable scores and short explanations that appear on event cards and detail pages.

## Why it exists
- **Trust & signal:** A concise, consistent score improves decision speed and quality.
- **Transparency:** Short "why" blurbs explain the score drivers.
- **Coaching:** Organizers learn what details improve discoverability and fit.

## Core Score Facets (MVP)
- **CommunityVibe™ (0–10):** Sense of togetherness, local flavor, inclusivity.
- **FamilyFun™ (0–10):** Suitability for families and kids.
- **Overall (0–10):** Weighted blend of the facets above (simple average in MVP).

> Note: Use **Funalytics™** (™ until registered). Keep capitalization consistent across UI and docs.

## Where it shows up
- Event card (compact): Overall + 1–2 facet badges
- Event detail page: All facets + short rationale ("because…")
- Organizer dashboard (later): Score preview + coaching tips

## When it's computed
- On event creation (first pass)
- On event edit (recompute)
- On scheduled refresh jobs (e.g., nightly) if details changed materially

## High-level flow (MVP)
Event data ➜ sanitize/validate ➜ facet computations ➜ overall score ➜ compact summary ➜ store historical rows ➜ show latest on UI
