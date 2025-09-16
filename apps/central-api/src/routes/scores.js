/**
 * Unified Scores API Routes
 * Supports both legacy Funalytics and generic multi-brand scoring systems
 */

const { Router } = require('express');
const { PrismaClient } = require('../../generated/prisma');
const { adapterRegistry } = require('../adapters');

const router = Router();
const prisma = new PrismaClient();

/**
 * LEGACY FUNALYTICS ROUTES (for backward compatibility)
 * These routes handle legacy /funalytics/* calls with simplified parameters
 */

/**
 * GET /latest - Legacy Funalytics route (when mounted under /funalytics)
 * Only requires entityType parameter, defaults to funlist + Funalytics
 */
router.get('/latest', async (req, res) => {
  try {
    console.log('[LEGACY] GET /latest called with query:', req.query);
    const { entityType, entityId, limit = '10' } = req.query;
    
    // Check if this is a legacy call (missing brand/system) vs generic call
    const { brand, system } = req.query;
    const isLegacyCall = !brand && !system;
    
    if (isLegacyCall) {
      // Legacy behavior: only entityType required
      if (!entityType) {
        return res.status(400).json({
          success: false,
          error: 'Missing required parameter: entityType'
        });
      }
      
      console.log('[LEGACY] Processing legacy funalytics request');
      
      // Use fixed values for legacy Funalytics
      var whereConditions = {
        brand: 'funlist',
        system: 'Funalytics',
        entityType
      };
    } else {
      // Generic behavior: brand, system, entityType required
      if (!brand || !system || !entityType) {
        return res.status(400).json({
          success: false,
          error: 'Missing required parameters: brand, system, entityType'
        });
      }
      
      console.log('[GENERIC] Processing generic scores request');
      
      // Validate brand and system
      const validBrands = ['funlist', 'businesscalendar'];
      const validSystems = adapterRegistry.getSupportedSystems();
      
      if (!validBrands.includes(brand)) {
        return res.status(400).json({
          success: false,
          error: `Invalid brand. Supported: ${validBrands.join(', ')}`
        });
      }
      
      if (!validSystems.includes(system)) {
        return res.status(400).json({
          success: false,
          error: `Invalid system. Supported: ${validSystems.join(', ')}`
        });
      }
      
      var whereConditions = {
        brand,
        system,
        entityType
      };
    }
    
    if (entityId) {
      whereConditions.entityId = parseInt(entityId);
    }

    // Get latest scores per entity
    const latestTimestamps = await prisma.score.groupBy({
      by: ['entityId'],
      where: whereConditions,
      _max: {
        computedAt: true
      }
    });

    const entityIds = latestTimestamps.map(item => item.entityId);
    const scores = await prisma.score.findMany({
      where: {
        ...whereConditions,
        entityId: { in: entityIds },
        OR: latestTimestamps.map(item => ({
          entityId: item.entityId,
          computedAt: item._max.computedAt
        }))
      },
      orderBy: { computedAt: 'desc' },
      take: parseInt(limit)
    });

    // Format response based on call type
    if (isLegacyCall) {
      // Legacy format with additional fields
      const legacyData = scores.map(score => ({
        id: score.id,
        entityType: score.entityType,
        entityId: score.entityId,
        overallScore: score.overallScore,
        dimensions: score.dimensions,
        reasoning: score.reasoning,
        computedAt: score.computedAt,
        // Legacy format fields
        fun_rating: score.overallScore,
        fun_meter: Math.round(score.overallScore)
      }));

      return res.json({
        success: true,
        data: legacyData,
        pagination: {
          page: 1,
          limit: parseInt(limit),
          total: legacyData.length,
          pages: 1
        }
      });
    } else {
      // Generic format
      const total = await prisma.score.count({
        where: whereConditions
      });
      
      return res.json({
        success: true,
        data: scores,
        pagination: {
          page: 1,
          limit: parseInt(limit),
          total,
          pages: Math.ceil(total / parseInt(limit))
        }
      });
    }

  } catch (error) {
    console.error('Error fetching scores:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch scores',
      message: error.message
    });
  }
});

/**
 * POST /compute - Legacy Funalytics + Generic route
 * Handles both legacy (entityType, entityId) and generic (brand, system, entityType, entityId) calls
 */
router.post('/compute', async (req, res) => {
  try {
    console.log('[COMPUTE] POST /compute called with body:', req.body);
    const { entityType, entityId, forceRecompute = false } = req.body;
    
    // Check if this is a legacy call vs generic call
    const { brand, system } = req.body;
    const isLegacyCall = !brand && !system;
    
    if (isLegacyCall) {
      // Legacy behavior: only entityType, entityId required
      if (!entityType || !entityId) {
        return res.status(400).json({
          success: false,
          error: 'Missing required parameters: entityType, entityId'
        });
      }
      
      console.log('[LEGACY] Processing legacy funalytics compute');
      
      // Use fixed values for legacy Funalytics
      var finalBrand = 'funlist';
      var finalSystem = 'Funalytics';
    } else {
      // Generic behavior: brand, system, entityType, entityId required
      if (!brand || !system || !entityType || !entityId) {
        return res.status(400).json({
          success: false,
          error: 'Missing required parameters: brand, system, entityType, entityId'
        });
      }
      
      console.log('[GENERIC] Processing generic compute');
      
      // Validate system adapter exists
      if (!adapterRegistry.isSupported(system)) {
        return res.status(400).json({
          success: false,
          error: `Unsupported scoring system: ${system}`
        });
      }
      
      var finalBrand = brand;
      var finalSystem = system;
    }

    // Check if score already exists (unless forced recompute)
    if (!forceRecompute) {
      const existingScore = await prisma.score.findFirst({
        where: {
          brand: finalBrand,
          system: finalSystem,
          entityType,
          entityId: parseInt(entityId)
        },
        orderBy: { computedAt: 'desc' }
      });

      if (existingScore && existingScore.status === 'completed') {
        if (isLegacyCall) {
          return res.json({
            success: true,
            data: {
              id: existingScore.id,
              entityType: existingScore.entityType,
              entityId: existingScore.entityId,
              overallScore: existingScore.overallScore,
              dimensions: existingScore.dimensions,
              reasoning: existingScore.reasoning,
              computedAt: existingScore.computedAt,
              // Legacy format fields
              fun_rating: existingScore.overallScore,
              fun_meter: Math.round(existingScore.overallScore)
            },
            cached: true
          });
        } else {
          return res.json({
            success: true,
            data: existingScore,
            cached: true
          });
        }
      }
    }

    // Create temporary entity data for scoring
    const entity = {
      id: parseInt(entityId),
      title: `Sample ${entityType} ${entityId}`,
      description: `Sample description for ${entityType} scoring`,
      category: 'general',
      city: 'Sample City',
      state: 'Sample State'
    };

    // Get the appropriate scoring adapter
    const adapter = adapterRegistry.getAdapter(finalSystem);

    // Compute the score
    const scoreResult = await adapter.computeScore({
      entityType,
      entity
    });

    // Save the score to database
    const savedScore = await prisma.score.create({
      data: {
        brand: finalBrand,
        system: finalSystem,
        entityType,
        entityId: parseInt(entityId),
        overallScore: scoreResult.overallScore,
        dimensions: scoreResult.dimensions,
        reasoning: scoreResult.reasoning,
        status: scoreResult.status,
        computedAt: new Date()
      }
    });

    // Return data based on call type
    if (isLegacyCall) {
      // Legacy format
      return res.json({
        success: true,
        data: {
          id: savedScore.id,
          entityType: savedScore.entityType,
          entityId: savedScore.entityId,
          overallScore: savedScore.overallScore,
          dimensions: savedScore.dimensions,
          reasoning: savedScore.reasoning,
          computedAt: savedScore.computedAt,
          // Legacy format fields
          fun_rating: savedScore.overallScore,
          fun_meter: Math.round(savedScore.overallScore)
        },
        cached: false
      });
    } else {
      // Generic format
      return res.json({
        success: true,
        data: savedScore,
        cached: false
      });
    }

  } catch (error) {
    console.error('Error computing score:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to compute score',
      message: error.message
    });
  }
});

module.exports = router;