# Overview

FunList.ai is an AI-powered event discovery platform built with Flask that helps users find fun activities in their area. The platform features a sophisticated "Fun Rating System" (1-5 scale) to help users discover events based on their potential for entertainment value. It serves as a comprehensive hub for event organizers, attendees, and sponsors to connect through event listings, advertising opportunities, and community engagement.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Architecture
The application uses Flask as the primary web framework with SQLAlchemy for database operations. The architecture follows a traditional MVC pattern with separate modules for routes, models, and forms. The database schema supports multiple user types (event creators, organizers, vendors, sponsors) with role-based permissions managed through boolean flags on the User model.

## Database Design
The system uses a PostgreSQL database with SQLAlchemy ORM. Key models include User, Event, Subscriber, and various support tables. The User model implements a flexible role system allowing users to have multiple roles (organizer, vendor, sponsor, admin). Events contain geolocation data (latitude/longitude) for map-based discovery and include the core "fun_meter" rating field for the Fun Rating System.

## Authentication & Authorization
User authentication is handled through Flask-Login with password hashing via Werkzeug. The system implements role-based access control with decorators for admin, organizer, sponsor, and other privilege levels. CSRF protection is enabled through Flask-WTF, and session management uses Flask-Session.

## Event Discovery System
Events are discoverable through both list and map views using Leaflet.js for interactive mapping. The featured events API (`/api/featured-events`) leverages the Fun Rating System by filtering events with fun_meter >= 4 and calculating distance-based recommendations within a 15-mile radius. Geolocation is used to show nearby high-fun events to users.

## Frontend Architecture
The frontend uses server-side rendering with Jinja2 templates and Bootstrap for responsive design. Interactive maps are powered by Leaflet.js, and the application includes custom CSS for styling. JavaScript is used for dynamic interactions and AJAX calls to backend APIs.

## Fun Rating Algorithm
The core differentiator is the Fun Rating System that assigns events a 1-5 star rating based on entertainment value. Event organizers provide initial self-assessments, which can be verified by admin review. High-rated events (4+ stars) are eligible for "featured" status and appear in the featured events API for enhanced discovery.

# OAuth Implementation

## Security Features
The application implements OAuth 2.0 authentication with both Google and GitHub providers using industry-standard security practices:
- **PKCE (Proof Key for Code Exchange)**: Both OAuth providers implement PKCE flow for enhanced security against authorization code interception attacks
- **CSRF Protection**: State parameter validation to prevent cross-site request forgery
- **Session Management**: Secure session handling with one-time use code verifiers

## OAuth Configuration
- **Google OAuth**: Fully configured with PKCE, requires GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET environment variables
- **GitHub OAuth**: Fully configured with PKCE, requires GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET environment variables
- **Redirect URIs**: Both providers use `/google_login/callback` and `/auth/github/callback` endpoints respectively

# External Dependencies

## Core Framework Dependencies
- **Flask**: Web framework with extensions for login, forms, sessions, and CSRF protection
- **SQLAlchemy**: Database ORM with PostgreSQL as the production database
- **Flask-Migrate**: Database migration management
- **psycopg2-binary**: PostgreSQL database adapter

## Frontend Libraries
- **Bootstrap 5.3.2**: CSS framework for responsive design
- **Leaflet.js 1.9.4**: Interactive mapping library
- **Font Awesome**: Icon library for UI elements

## API Integrations
- **Google Maps API**: Geocoding and location services (API key required - set GOOGLE_MAPS_API_KEY environment variable)
- **OpenAI API**: AI-powered features and recommendations
- **Stripe API**: Payment processing (planned implementation)

## Development & Deployment
- **Replit**: Primary hosting and development environment
- **psutil**: Process monitoring and management
- **scikit-learn & NumPy**: Machine learning capabilities for recommendation algorithms

## Security & Utilities
- **email-validator**: Email address validation
- **python-dateutil**: Date/time handling utilities
- **Flask-WTF**: CSRF protection and form handling
- **Werkzeug**: Password hashing and security utilities