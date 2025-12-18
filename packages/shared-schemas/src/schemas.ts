import { z } from 'zod';
import { ScoreSystemEnum, BrandEnum, EntityTypeEnum, ScoreStatusEnum } from './enums.js';

/**
 * Base score dimensions schema - flexible JSON structure
 */
export const ScoreDimensionsSchema = z.record(z.number().min(0).max(10));
export type ScoreDimensions = z.infer<typeof ScoreDimensionsSchema>;

/**
 * Generic score record schema
 */
export const ScoreRecordSchema = z.object({
  id: z.string().uuid().optional(),
  brand: BrandEnum,
  system: ScoreSystemEnum,
  entityType: EntityTypeEnum,
  entityId: z.number().int().positive(),
  overallScore: z.number().min(0).max(10),
  dimensions: ScoreDimensionsSchema,
  reasoning: z.string().max(500).optional(),
  status: ScoreStatusEnum.default('completed'),
  computedAt: z.date().optional(),
  createdAt: z.date().optional(),
  updatedAt: z.date().optional()
});
export type ScoreRecord = z.infer<typeof ScoreRecordSchema>;

/**
 * API request schema for computing scores
 */
export const ComputeScoreRequestSchema = z.object({
  brand: BrandEnum,
  system: ScoreSystemEnum,
  entityType: EntityTypeEnum,
  entityId: z.number().int().positive(),
  forceRecompute: z.boolean().default(false)
});
export type ComputeScoreRequest = z.infer<typeof ComputeScoreRequestSchema>;

/**
 * API request schema for fetching latest scores
 */
export const GetLatestScoreRequestSchema = z.object({
  brand: BrandEnum,
  system: ScoreSystemEnum,
  entityType: EntityTypeEnum,
  entityId: z.number().int().positive().optional(),
  limit: z.number().int().min(1).max(100).default(10)
});
export type GetLatestScoreRequest = z.infer<typeof GetLatestScoreRequestSchema>;

/**
 * API response schemas
 */
export const ScoreResponseSchema = z.object({
  success: z.boolean(),
  data: ScoreRecordSchema.optional(),
  error: z.string().optional()
});
export type ScoreResponse = z.infer<typeof ScoreResponseSchema>;

export const ScoresListResponseSchema = z.object({
  success: z.boolean(),
  data: z.array(ScoreRecordSchema).optional(),
  pagination: z.object({
    page: z.number().int().min(1),
    limit: z.number().int().min(1),
    total: z.number().int().min(0),
    pages: z.number().int().min(0)
  }).optional(),
  error: z.string().optional()
});
export type ScoresListResponse = z.infer<typeof ScoresListResponseSchema>;
