import React from 'react';
import { FunListEventContract } from '../types/events';
import EventCard from './EventCard';
import styles from './EventGrid.module.css';

interface EventGridProps {
  events: FunListEventContract[];
}

export default function EventGrid({ events }: EventGridProps) {
  if (!events || !Array.isArray(events) || events.length === 0) {
    return (
      <div className={styles.emptyState}>
        No events found right now. Check back later!
      </div>
    );
  }

  return (
    <div className={styles.grid}>
      {events.map((event, index) => (
        <EventCard key={event.id ? `${event.id}-${index}` : index} event={event} />
      ))}
    </div>
  );
}
