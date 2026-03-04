/**
 * Frontend Event Types mappings
 * Demonstrates the spatial data contracts (Map UI) for the frontend 
 * as well as the AI metadata block.
 */

export interface MapBoundary {
  north: number;
  south: number;
  east: number;
  west: number;
}

export interface FunListEventContract {
  id: string;
  title: string;
  description: string;
  date: string;
  startTime: string;
  endTime: string;
  
  venueName: string;
  address: string;
  city: string;
  state: string;
  
  // ---- REQUIRED SPATIAL FIELDS FOR THE FRONTEND MAPS UI ----
  // These fields MUST be present in the JSON payload returned by the Google Cloud Run API
  latitude: number | null;
  longitude: number | null;
  // ------------------------------------------------------------
  
  organizerName: string;
  price: number | null;
  isFree: boolean;
  
  // Sister site affinity (Is this a BusinessCalendar event or purely FunList?)
  originSite: string; // 'funlist' | 'bcal'
  visibilityTags: string[]; // ['funlist', 'bcal']
  
  // AI Enrichment 
  confidenceScore: number;
  isAiEnriched: boolean;
}

// Example usage by the map rendering loop:
export function isEventInBoundaries(event: FunListEventContract, bounds: MapBoundary): boolean {
  if (!event.latitude || !event.longitude) return false;
  
  return (
    event.latitude <= bounds.north &&
    event.latitude >= bounds.south &&
    event.longitude <= bounds.east &&
    event.longitude >= bounds.west
  );
}
