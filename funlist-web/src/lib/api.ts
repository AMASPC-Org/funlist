import 'server-only';
import { FunListEventContract } from '../types/events';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

export interface EventData {
  id: string;
  title: string;
  description: string;
  date: string;
  location: string;
  origin_site: string;
  confidence_score: number;
}

/**
 * Fetches events specifically filtered for the Funlist ecosystem
 */
export async function getFunlistEvents(): Promise<EventData[]> {
  try {
    // We attach origin_site=funlist as mandated by the shared backend
    const res = await fetch(`${API_BASE_URL}/events?origin_site=funlist`, {
      next: { revalidate: 60 } // Cache for 1 minute
    });
    
    if (!res.ok) {
      throw new Error(`Failed to fetch events: ${res.statusText}`);
    }
    
    return await res.json();
  } catch (error) {
    console.error("Error fetching Funlist events:", error);
    return [];
  }
}

/**
 * Fetches heavily curated "Featured Finds" with high confidence scores
 */
export async function getFeaturedEvents(): Promise<EventData[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/events?origin_site=funlist&featured=true`, {
      next: { revalidate: 300 } 
    });
    
    if (!res.ok) throw new Error('Failed to fetch featured events');
    return await res.json();
  } catch (error) {
    console.error("Error fetching Featured events:", error);
    return [];
  }
}

/**
 * Fetches events tailored for the Map UI with strict typed contract 
 */
export async function fetchEventsForMap(): Promise<FunListEventContract[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/events?origin_site=funlist`, {
      next: { revalidate: 60 }
    });
    
    if (!res.ok) {
      console.error('Failed to fetch map events:', res.statusText);
      return [];
    }
    
    const data = await res.json();
    return data as FunListEventContract[];
  } catch (error) {
    console.error("Error fetching map events:", error);
    return [];
  }
}
