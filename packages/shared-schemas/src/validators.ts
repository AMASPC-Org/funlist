import { z } from 'zod';
import { 
  ComputeScoreRequestSchema, 
  GetLatestScoreRequestSchema, 
  ScoreRecordSchema 
} from './schemas.js';

/**
 * Validation helpers for API endpoints
 */

export const validateComputeScoreRequest = (data: unknown) => {
  return ComputeScoreRequestSchema.safeParse(data);
};

export const validateGetLatestScoreRequest = (data: unknown) => {
  return GetLatestScoreRequestSchema.safeParse(data);
};

export const validateScoreRecord = (data: unknown) => {
  return ScoreRecordSchema.safeParse(data);
};

/**
 * Middleware helper for Express validation
 */
export const createValidationMiddleware = (schema: z.ZodSchema) => {
  return (req: any, res: any, next: any) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({
        success: false,
        error: 'Validation failed',
        details: result.error.issues
      });
    }
    req.validatedData = result.data;
    next();
  };
};