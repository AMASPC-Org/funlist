/**
 * OpenAPI 3.0 specifications for the Scores API
 */

export const ScoresAPIOpenAPI = {
  openapi: '3.0.0',
  info: {
    title: 'Multi-Brand Scores API',
    version: '1.0.0',
    description: 'Generic scoring system supporting multiple brands and scoring algorithms'
  },
  servers: [
    {
      url: 'http://localhost:3001',
      description: 'Development server'
    }
  ],
  paths: {
    '/scores/latest': {
      get: {
        summary: 'Get latest scores',
        description: 'Retrieve latest scores for specified brand, system, and entity',
        parameters: [
          {
            name: 'brand',
            in: 'query',
            required: true,
            schema: { type: 'string', enum: ['funlist', 'businesscalendar'] }
          },
          {
            name: 'system',
            in: 'query', 
            required: true,
            schema: { type: 'string', enum: ['Funalytics', 'ConnectScore', 'Elevate'] }
          },
          {
            name: 'entityType',
            in: 'query',
            required: true,
            schema: { type: 'string', enum: ['event', 'venue', 'experience'] }
          },
          {
            name: 'entityId',
            in: 'query',
            required: false,
            schema: { type: 'integer', minimum: 1 }
          },
          {
            name: 'limit',
            in: 'query',
            required: false,
            schema: { type: 'integer', minimum: 1, maximum: 100, default: 10 }
          }
        ],
        responses: {
          '200': {
            description: 'Successful response',
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  properties: {
                    success: { type: 'boolean' },
                    data: {
                      type: 'array',
                      items: { $ref: '#/components/schemas/ScoreRecord' }
                    },
                    pagination: { $ref: '#/components/schemas/Pagination' }
                  }
                }
              }
            }
          }
        }
      }
    },
    '/scores/compute': {
      post: {
        summary: 'Compute score',
        description: 'Trigger score computation for specified entity',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: { $ref: '#/components/schemas/ComputeScoreRequest' }
            }
          }
        },
        responses: {
          '200': {
            description: 'Score computed successfully',
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/ScoreResponse' }
              }
            }
          }
        }
      }
    }
  },
  components: {
    schemas: {
      ScoreRecord: {
        type: 'object',
        properties: {
          id: { type: 'string', format: 'uuid' },
          brand: { type: 'string', enum: ['funlist', 'businesscalendar'] },
          system: { type: 'string', enum: ['Funalytics', 'ConnectScore', 'Elevate'] },
          entityType: { type: 'string', enum: ['event', 'venue', 'experience'] },
          entityId: { type: 'integer', minimum: 1 },
          overallScore: { type: 'number', minimum: 0, maximum: 10 },
          dimensions: { 
            type: 'object', 
            additionalProperties: { type: 'number', minimum: 0, maximum: 10 }
          },
          reasoning: { type: 'string', maxLength: 500 },
          status: { type: 'string', enum: ['pending', 'computing', 'completed', 'failed'] },
          computedAt: { type: 'string', format: 'date-time' },
          createdAt: { type: 'string', format: 'date-time' },
          updatedAt: { type: 'string', format: 'date-time' }
        }
      },
      ComputeScoreRequest: {
        type: 'object',
        required: ['brand', 'system', 'entityType', 'entityId'],
        properties: {
          brand: { type: 'string', enum: ['funlist', 'businesscalendar'] },
          system: { type: 'string', enum: ['Funalytics', 'ConnectScore', 'Elevate'] },
          entityType: { type: 'string', enum: ['event', 'venue', 'experience'] },
          entityId: { type: 'integer', minimum: 1 },
          forceRecompute: { type: 'boolean', default: false }
        }
      },
      ScoreResponse: {
        type: 'object',
        properties: {
          success: { type: 'boolean' },
          data: { $ref: '#/components/schemas/ScoreRecord' },
          error: { type: 'string' }
        }
      },
      Pagination: {
        type: 'object',
        properties: {
          page: { type: 'integer', minimum: 1 },
          limit: { type: 'integer', minimum: 1 },
          total: { type: 'integer', minimum: 0 },
          pages: { type: 'integer', minimum: 0 }
        }
      }
    }
  }
};
