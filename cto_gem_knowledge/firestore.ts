import { Firestore, GeoPoint, Timestamp } from '@google-cloud/firestore';

// Initialize Firestore using ADC
// Notice no credentials passed, it authenticates via GCP metadata server natively
const firestore = new Firestore();

/**
 * Enterprise Data Contract for Firestore venues
 */
export interface FirestoreVenue {
  id: string; // Document ID
  name: string;
  address: string | null;
  city: string | null;
  county: string | null;
  state: string | null;
  postalCode: string | null;
  
  // Notice GeoPoint usage for fast coordinate bounds lookup
  location: GeoPoint | null; 
  
  websiteUrl: string | null;
  originSite: string; // e.g. 'bcal', 'funlist'
  createdAt: Timestamp;
}

/**
 * Enterprise Data Contract for Firestore events
 */
export interface FirestoreEvent {
  id: string; // Document ID
  title: string;
  description: string | null;
  eventType: string;
  
  startDate: Timestamp;
  endDate: Timestamp | null;
  
  venueId: string; // Document reference to /venues/{id}
  venueName: string | null;
  
  // Duplicated locally on the event object so the frontend Map UI can easily draw markers without a second hop
  location: GeoPoint | null; 
  
  organizerName: string | null;
  price: number | null;
  isFree: boolean;
  status: 'pending' | 'approved' | 'rejected';
  
  // ---- AI Enrichment & Validation Block ----
  confidenceScore: number;
  isAiEnriched: boolean;
  enrichmentData: any | null; // e.g., categories predicted by the LLM
  
  // ---- Cross-site ecosystem config ----
  originSite: string;
  visibilityTags: string[]; // Access tags mapping to sites like ['funlist', 'bcal']
  
  createdAt: Timestamp;
}

// Global Collection References
export const stagingDraftsCollection = firestore.collection('staging_drafts');
export const productionEventsCollection = firestore.collection('production_events');
export const venuesCollection = firestore.collection('venues');
export const organizationsCollection = firestore.collection('organizations');

/**
 * Example helper demonstrating how we prepare a document for saving to Firestore
 * Maps properties like latitude/longitude to a proper GeoPoint
 */
export function buildFirestoreEvent(eventData: any, lat: number, lng: number): FirestoreEvent {
  return {
    ...eventData,
    location: new GeoPoint(lat, lng), // Spatial mapping applied here!
    startDate: Timestamp.fromDate(new Date(eventData.startDate)),
    createdAt: Timestamp.now(),
  };
}
