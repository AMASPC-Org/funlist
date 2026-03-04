import React from 'react';
import { FunListEventContract } from '../types/events';
import styles from './EventCard.module.css';

interface EventCardProps {
  event: FunListEventContract;
}

export default function EventCard({ event }: EventCardProps) {
  const displayPrice = event.isFree 
    ? 'Free' 
    : (typeof event.price === 'number' ? `$${event.price.toFixed(2)}` : 'Pricing Unavailable');
  
  let formattedDate = event.date || 'Date TBD';
  try {
    const dateMatch = event.date ? String(event.date).match(/^(\d{4})-(\d{2})-(\d{2})/) : null;
    if (dateMatch) {
      const year = parseInt(dateMatch[1], 10);
      const month = parseInt(dateMatch[2], 10) - 1;
      const day = parseInt(dateMatch[3], 10);
      const d = new Date(year, month, day);
      if (!isNaN(d.getTime())) {
        formattedDate = new Intl.DateTimeFormat('en-US', {
          month: 'short',
          day: 'numeric',
          year: 'numeric'
        }).format(d);
      }
    } else if (event.date) {
      const d = new Date(event.date);
      if (!isNaN(d.getTime())) {
        formattedDate = new Intl.DateTimeFormat('en-US', {
          month: 'short',
          day: 'numeric',
          year: 'numeric'
        }).format(d);
      }
    }
  } catch {
    // Ignore and fallback to raw date string
  }

  return (
    <div className={styles.card}>
      <h3 className={styles.title}>{event.title || 'Untitled Event'}</h3>
      <div className={styles.metaRow}>
        <span className={styles.icon} role="img" aria-label="Date">📅</span>
        <span>
          {formattedDate}
          {event.startTime ? ` • ${event.startTime}` : ''}
        </span>
      </div>
      <div className={styles.metaRow}>
        <span className={styles.icon} role="img" aria-label="Venue">📍</span>
        <span className={styles.venue}>{event.venueName || 'Venue TBD'}</span>
      </div>
      <div className={event.isFree ? styles.priceBadge : `${styles.priceBadge} ${styles.priceBadgePaid}`}>
        {displayPrice}
      </div>
    </div>
  );
}
