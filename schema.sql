-- ====================================================
-- FunList.ai — PostgreSQL Schema (MVP Foundation)
-- ====================================================

-- Users (attendees, organizers, admins)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT CHECK (role IN ('attendee', 'organizer', 'admin')) DEFAULT 'attendee',
    display_name TEXT,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- Venues (where events are held)
CREATE TABLE venues (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    address TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT now()
);

-- Events (submitted by organizers or ingested)
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    venue_id UUID REFERENCES venues(id) ON DELETE SET NULL,
    organizer_id UUID REFERENCES users(id) ON DELETE CASCADE,
    status TEXT CHECK (status IN ('draft', 'pending', 'approved', 'rejected')) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- Funalytics Scores (per event, calculated by AI Assistant)
CREATE TABLE funalytics_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID REFERENCES events(id) ON DELETE CASCADE,
    community_vibe INTEGER CHECK (community_vibe BETWEEN 0 AND 10),
    family_fun INTEGER CHECK (family_fun BETWEEN 0 AND 10),
    overall_score INTEGER CHECK (overall_score BETWEEN 0 AND 10),
    reasoning TEXT,  -- short explanation string
    computed_at TIMESTAMP DEFAULT now()
);

-- Favorites (attendees saving events)
CREATE TABLE favorites (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    event_id UUID REFERENCES events(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT now(),
    PRIMARY KEY (user_id, event_id)
);

-- Basic Audit Log (admins & system events)
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action TEXT NOT NULL,
    target_type TEXT,
    target_id UUID,
    timestamp TIMESTAMP DEFAULT now()
);

-- Indexes for performance
CREATE INDEX idx_events_start_time ON events(start_time);
CREATE INDEX idx_events_status ON events(status);
CREATE INDEX idx_favorites_user_id ON favorites(user_id);
