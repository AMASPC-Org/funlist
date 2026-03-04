import React from 'react';
import { FunListEventContract } from '../types/events';

interface EventMapProps {
  events: FunListEventContract[];
}

export default function EventMap({ events }: EventMapProps) {
  return (
    <div style={{
      width: '100%',
      height: '300px',
      background: 'var(--bg-warm-white)',
      borderRadius: '12px',
      border: '1px solid var(--border-light)',
      position: 'relative',
      overflow: 'hidden',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }}>
      {events.length === 0 ? (
        <div style={{ color: 'var(--text-secondary)', fontWeight: 600 }}>
          Interactive Map: No events to display
        </div>
      ) : (
        <>
          <div style={{ position: 'absolute', top: '10px', left: '10px', background: 'rgba(255,255,255,0.9)', padding: '0.5rem', borderRadius: '8px', fontSize: '0.85rem', fontWeight: 600, zIndex: 10 }}>
            Mock Map View
          </div>
          {events.map(event => (
            event.latitude !== null && event.longitude !== null ? (
              <div 
                key={event.id}
                style={{
                  position: 'absolute',
                  // Mock plotting logic for visual purposes. Real mapping libraries would use LatLng.
                  left: `calc(50% + ${event.longitude * 2}px)`,
                  top: `calc(50% - ${event.latitude * 2}px)`,
                  width: '12px',
                  height: '12px',
                  backgroundColor: 'var(--primary-orange)',
                  borderRadius: '50%',
                  border: '2px solid white',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
                  cursor: 'pointer',
                  transform: 'translate(-50%, -50%)'
                }}
                title={`${event.title} (${event.latitude}, ${event.longitude})`}
              />
            ) : null
          ))}
        </>
      )}
    </div>
  );
}
