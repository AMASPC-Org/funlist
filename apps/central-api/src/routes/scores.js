/**
 * Generic Scores API Routes
 * Supports multiple brands and scoring systems
 */

const { Router } = require('express');
const { PrismaClient } = require('../../generated/prisma');
const { adapterRegistry } = require('../adapters');

const router = Router();
const prisma = new PrismaClient();

/**
 * BACKWARD COMPATIBILITY ROUTES - MUST COME FIRST!
 * Legacy /funalytics/* routes that provide direct implementation
 */

/**
 * GET /funalytics/latest
 * Legacy route for Funalytics scores - direct implementation
 */
router.get('/funalytics/latest', async (req, res) => {
  try {
    const { entityType, entityId, limit = '10' } = req.query;
    
    // Validate required parameters for legacy route
    if (!entityType) {
      return res.status(400).json({
        success: false,
        error: 'Missing required parameter: entityType'
      });
    }

    // Build query conditions for Funalytics on FunList
    const whereConditions = {
      brand: 'funlist',
      system: 'Funalytics',
      entityType
    };
    
    if (entityId) {
      whereConditions.entityId = parseInt(entityId);
    }

    // Get latest scores (implementation copied from generic route)
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

    // Transform to legacy format
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
    
  } catch (error) {
    console.error('Error in legacy funalytics route:', error);
    return res.status(500).json({
      success: false,
      error: error.message || 'Failed to fetch scores'
    });
  }
});

/**
 * POST /funalytics/compute
 * Legacy route for Funalytics score computation - direct implementation
 */
router.post('/funalytics/compute', async (req, res) => {
  try {
    const { entityType, entityId, forceRecompute = false } = req.body;
    
    // Validate required parameters
    if (!entityType || !entityId) {
      return res.status(400).json({
        success: false,
        error: 'Missing required parameters: entityType, entityId'
      });
    }

    // Set default values for Funalytics on FunList
    const brand = 'funlist';
    const system = 'Funalytics';

    // Check if score already exists (unless forced recompute) - copied from generic route
    if (!forceRecompute) {
      const existingScore = await prisma.score.findFirst({
        where: {
          brand,
          system,
          entityType,
          entityId: parseInt(entityId)
        },
        orderBy: { computedAt: 'desc' }
      });

      if (existingScore) {
        // Return existing score in legacy format
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
      }
    }

    // Temporary entity data for scoring (avoiding Event/Venue model dependency)
    const entity = {
      id: parseInt(entityId),
      title: `Sample ${entityType} ${entityId}`,
      description: `Sample description for ${entityType} scoring`,
      category: 'general',
      city: 'Sample City',
      state: 'Sample State'
    };

    // Get the Funalytics adapter
    const adapter = adapterRegistry.getAdapter(system);

    // Compute the score
    const scoreResult = await adapter.computeScore({
      entityType,
      entity
    });

    // Save the score to database
    const savedScore = await prisma.score.create({
      data: {
        brand,
        system,
        entityType,
        entityId: parseInt(entityId),
        overallScore: scoreResult.overallScore,
        dimensions: scoreResult.dimensions,
        reasoning: scoreResult.reasoning,
        status: scoreResult.status,
        computedAt: new Date()
      }
    });

    // Return in legacy format
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
    
  } catch (error) {
    console.error('Error in legacy funalytics compute:', error);
    return res.status(500).json({
      success: false,
      error: error.message || 'Failed to compute score'
    });
  }
});

/**
 * GENERIC MULTI-BRAND ROUTES
 * New generic scoring system supporting multiple brands and systems
 */

/**
 * GET /scores/latest
 * Fetch latest scores for specified brand, system, entityType, and optionally entityId
 */
router.get('/latest', async (req, res) => {
  try {
    const { brand, system, entityType, entityId, limit = '10' } = req.query;
    
    // Validate required parameters
    if (!brand || !system || !entityType) {
      return res.status(400).json({
        success: false,
        error: 'Missing required parameters: brand, system, entityType'
      });
    }

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

    // Build query conditions
    const whereConditions = {
      brand,
      system,
      entityType
    };
    
    if (entityId) {
      whereConditions.entityId = parseInt(entityId);
    }

    // Fetch latest scores per entity (proper implementation)
    // First get the latest computedAt for each entity
    const latestTimestamps = await prisma.score.groupBy({
      by: ['entityId'],
      where: whereConditions,
      _max: {
        computedAt: true
      }
    });

    // Then fetch the actual scores using those timestamps
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
      orderBy: { computedAt: 'desc' }
    });

    const total = await prisma.score.count({
      where: whereConditions
    });

    res.json({
      success: true,
      data: scores,
      pagination: {
        page: 1,
        limit: parseInt(limit),
        total,
        pages: Math.ceil(total / parseInt(limit))
      }
    });

  } catch (error) {
    console.error('Error fetching latest scores:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch scores'
    });
  }
});

/**
 * POST /scores/compute
 * Trigger score computation for specified entity
 */
router.post('/compute', async (req, res) => {
  try {
    const { brand, system, entityType, entityId, forceRecompute = false } = req.body;
    
    // Validate required parameters
    if (!brand || !system || !entityType || !entityId) {
      return res.status(400).json({
        success: false,
        error: 'Missing required parameters: brand, system, entityType, entityId'
      });
    }

    // Validate system adapter exists
    if (!adapterRegistry.isSupported(system)) {
      return res.status(400).json({
        success: false,
        error: `Unsupported scoring system: ${system}`
      });
    }

    // Check if score already exists (unless forced recompute)
    if (!forceRecompute) {
      const existingScore = await prisma.score.findFirst({
        where: {
          brand,
          system,
          entityType,
          entityId: parseInt(entityId)
        },
        orderBy: { computedAt: 'desc' }
      });

      if (existingScore && existingScore.status === 'completed') {
        return res.json({
          success: true,
          data: existingScore,
          cached: true
        });
      }
    }

    // Temporary entity data for scoring (avoiding Event/Venue model dependency)
    const entity = {
      id: parseInt(entityId),
      title: `Sample ${entityType} ${entityId}`,
      description: `Sample description for ${entityType} scoring`,
      category: 'general',
      city: 'Sample City',
      state: 'Sample State'
    };

    // Get the appropriate scoring adapter
    const adapter = adapterRegistry.getAdapter(system);

    // Compute the score
    const scoreResult = await adapter.computeScore({
      entityType,
      entity
    });

    // Save the score to database
    const savedScore = await prisma.score.create({
      data: {
        brand,
        system,
        entityType,
        entityId: parseInt(entityId),
        overallScore: scoreResult.overallScore,
        dimensions: scoreResult.dimensions,
        reasoning: scoreResult.reasoning,
        status: scoreResult.status,
        computedAt: new Date()
      }
    });

    res.json({
      success: true,
      data: savedScore,
      cached: false
    });

  } catch (error) {
    console.error('Error computing score:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to compute score'
    });
  }
});

module.exports = router;