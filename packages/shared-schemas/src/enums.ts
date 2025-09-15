import { z } from 'zod';

/**
 * Supported scoring systems across brands
 */
export const ScoreSystemEnum = z.enum(['Funalytics', 'ConnectScore', 'Elevate']);
export type ScoreSystem = z.infer<typeof ScoreSystemEnum>;

/**
 * Supported brands in the platform
 */
export const BrandEnum = z.enum(['funlist', 'businesscalendar']);
export type Brand = z.infer<typeof BrandEnum>;

/**
 * Entity types that can be scored
 */
export const EntityTypeEnum = z.enum(['event', 'venue', 'experience']);
export type EntityType = z.infer<typeof EntityTypeEnum>;

/**
 * Score computation status
 */
export const ScoreStatusEnum = z.enum(['pending', 'computing', 'completed', 'failed']);
export type ScoreStatus = z.infer<typeof ScoreStatusEnum>;