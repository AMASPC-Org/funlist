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
