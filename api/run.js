// Simple API runner with better port handling
require('dotenv').config({ override: true });

const express = require('express');
const { PrismaClient } = require('./generated/prisma');

console.log('Starting FunList Express API...');

const app = express();
const prisma = new PrismaClient();

// Use port 3001 exclusively for our API
const PORT = 3001;

// Middleware
app.use(express.json());

// CORS middleware
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
  
  if (req.method === 'OPTIONS') {
    res.sendStatus(200);
  } else {
    next();
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    message: 'FunList API is running',
    timestamp: new Date().toISOString(),
    port: PORT
  });
});

// Input validation helper
const validateEventData = (data) => {
  const errors = [];
  
  if (!data.title || data.title.trim().length === 0) {
    errors.push('Title is required');
  }
  
  if (!data.startTime) {
    errors.push('Start time is required');
  }
  
  if (data.startTime && data.endTime) {
    const startDate = new Date(data.startTime);
    const endDate = new Date(data.endTime);
    
    if (startDate >= endDate) {
      errors.push('Start time must be before end time');
    }
  }
  
  if (!data.organizerId) {
    errors.push('Organizer ID is required');
  }
  
  return errors;
};

// Funalytics™ MVP Heuristic Scoring Functions
const computeFunalyticsScore = (event) => {
  const title = (event.title || '').toLowerCase();
  const description = (event.description || '').toLowerCase();
  const category = (event.category || '').toLowerCase();
  const targetAudience = (event.target_audience || '').toLowerCase();
  const tags = (event.tags || '').toLowerCase();
  const city = (event.city || '').toLowerCase();
  const state = (event.state || '').toLowerCase();
  
  // Combine all text for easier searching
  const allText = `${title} ${description} ${category} ${targetAudience} ${tags}`;
  
  // CommunityVibe™ (0–10): Sense of togetherness, local flavor, inclusivity
  let communityVibe = 4; // Base score
  
  // +2 for local/community keywords
  const communityKeywords = ['local', 'community', 'neighborhood', 'town', 'city', 'nonprofit', 'volunteer', 'charity', 'fundraiser', 'civic'];
  if (communityKeywords.some(keyword => allText.includes(keyword))) {
    communityVibe += 2;
  }
  
  // +2 for nonprofit/community organization indicators
  const nonprofitKeywords = ['nonprofit', 'non-profit', 'community center', 'library', 'church', 'school', 'organization', 'foundation'];
  if (nonprofitKeywords.some(keyword => allText.includes(keyword))) {
    communityVibe += 2;
  }
  
  // +1 for smaller venue indicators (community spaces vs large commercial venues)
  const smallVenueKeywords = ['center', 'hall', 'room', 'park', 'garden', 'cafe', 'shop'];
  if (smallVenueKeywords.some(keyword => allText.includes(keyword))) {
    communityVibe += 1;
  }
  
  // Cap at 10
  communityVibe = Math.min(communityVibe, 10);
  
  // FamilyFun™ (0–10): Suitability for families and kids
  let familyFun = 4; // Base score
  
  // +3 for family/kid friendly keywords
  const familyKeywords = ['family', 'kid', 'kids', 'children', 'child', 'all ages', 'family-friendly', 'toddler', 'baby', 'parent'];
  if (familyKeywords.some(keyword => allText.includes(keyword))) {
    familyFun += 3;
  }
  
  // -2 for explicit 21+ content
  const adultOnlyKeywords = ['21+', '21 and up', 'adults only', 'adult only', 'mature', 'nightclub', 'bar crawl'];
  if (adultOnlyKeywords.some(keyword => allText.includes(keyword))) {
    familyFun -= 2;
  }
  
  // +1 for educational/activity keywords
  const educationalKeywords = ['learn', 'workshop', 'class', 'educational', 'craft', 'story', 'reading', 'game'];
  if (educationalKeywords.some(keyword => allText.includes(keyword))) {
    familyFun += 1;
  }
  
  // Cap at 0-10 range
  familyFun = Math.max(0, Math.min(familyFun, 10));
  
  // Overall Score: simple average of available facets (round to nearest int)
  const availableFacets = [communityVibe, familyFun].filter(score => score !== null && score !== undefined);
  const overallScore = availableFacets.length > 0 
    ? Math.round(availableFacets.reduce((sum, score) => sum + score, 0) / availableFacets.length)
    : 5; // Default if no facets available
  
  // Generate reasoning
  const reasons = [];
  if (communityVibe >= 7) reasons.push('strong community vibes');
  if (familyFun >= 7) reasons.push('family-friendly activities');
  if (communityKeywords.some(keyword => allText.includes(keyword))) reasons.push('local focus');
  if (familyKeywords.some(keyword => allText.includes(keyword))) reasons.push('great for kids');
  
  const reasoning = reasons.length > 0 
    ? `High fun score because of ${reasons.join(', ')}.`
    : 'Computed based on event details and keywords.';
  
  // Ensure reasoning is <= 240 chars
  const finalReasoning = reasoning.length > 240 ? reasoning.substring(0, 237) + '...' : reasoning;
  
  return {
    communityVibe,
    familyFun,
    overallScore,
    reasoning: finalReasoning
  };
};

// GET /events - returns all events with venue, organizer, and funalytics scores
app.get('/events', async (req, res) => {
  try {
    console.log('GET /events requested with query:', req.query);
    
    // Parse pagination parameters
    const page = parseInt(req.query.page) || 1;
    const limit = Math.min(parseInt(req.query.limit) || 20, 100);
    const offset = (page - 1) * limit;

    // Parse and validate filter parameters
    const { title, start, end, location } = req.query;
    
    // Build where clause for filtering
    const whereClause = {};
    
    // Title filter (partial match, case-insensitive)
    if (title) {
      if (typeof title !== 'string') {
        return res.status(400).json({
          success: false,
          error: 'Title filter must be a string'
        });
      }
      whereClause.title = {
        contains: title,
        mode: 'insensitive'
      };
    }
    
    // Date range filter
    if (start || end) {
      whereClause.start_date = {};
      let startDate, endDate;
      
      if (start) {
        startDate = new Date(start + 'T00:00:00.000Z'); // Ensure UTC
        if (isNaN(startDate.getTime())) {
          return res.status(400).json({
            success: false,
            error: 'Invalid start date format. Use YYYY-MM-DD'
          });
        }
        whereClause.start_date.gte = startDate;
      }
      
      if (end) {
        endDate = new Date(end + 'T23:59:59.999Z'); // Ensure UTC end of day
        if (isNaN(endDate.getTime())) {
          return res.status(400).json({
            success: false,
            error: 'Invalid end date format. Use YYYY-MM-DD'
          });
        }
        whereClause.start_date.lte = endDate;
      }
      
      // Validate date range if both provided
      if (startDate && endDate && startDate > endDate) {
        return res.status(400).json({
          success: false,
          error: 'Start date must be before or equal to end date'
        });
      }
    }
    
    // Location filter (search in city or state)
    if (location) {
      if (typeof location !== 'string') {
        return res.status(400).json({
          success: false,
          error: 'Location filter must be a string'
        });
      }
      whereClause.OR = [
        {
          city: {
            contains: location,
            mode: 'insensitive'
          }
        },
        {
          state: {
            contains: location,
            mode: 'insensitive'
          }
        },
        {
          venue: {
            is: {
              city: {
                contains: location,
                mode: 'insensitive'
              }
            }
          }
        },
        {
          venue: {
            is: {
              state: {
                contains: location,
                mode: 'insensitive'
              }
            }
          }
        }
      ];
    }

    const events = await prisma.events.findMany({
      where: whereClause,
      skip: offset,
      take: limit,
      include: {
        user: {
          select: {
            id: true,
            first_name: true,
            last_name: true,
            company_name: true,
            email: true
          }
        },
        venue: {
          select: {
            id: true,
            name: true,
            street: true,
            city: true,
            state: true,
            zip_code: true,
          }
        }
      },
      orderBy: {
        created_at: 'desc'
      }
    });

    const totalEvents = await prisma.events.count({
      where: whereClause
    });
    
    console.log(`Found ${events.length} real events from database`);

    res.json({
      success: true,
      count: events.length,
      events: events.map(event => ({
        id: event.id,
        title: event.title,
        description: event.description,
        startTime: event.start_date,
        endTime: event.end_date,
        location: event.location,
        city: event.city,
        state: event.state,
        category: event.category,
        funalyticsScore: {
          fun_rating: event.fun_rating,
          fun_meter: event.fun_meter
        },
        organizer: event.user,
        venue: event.venue,
        status: event.status,
        created_at: event.created_at
      })),
      pagination: {
        page,
        limit,
        total: totalEvents,
        pages: Math.ceil(totalEvents / limit)
      }
    });
  } catch (error) {
    console.error('Error fetching events:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to fetch events',
      message: error.message 
    });
  }
});

// POST /events - create a new event
app.post('/events', async (req, res) => {
  try {
    console.log('POST /events requested with data:', req.body);
    
    const { title, description, startTime, endTime, venue, organizerId } = req.body;
    
    // Validate input
    const validationErrors = validateEventData({ title, startTime, endTime, organizerId });
    if (validationErrors.length > 0) {
      return res.status(400).json({ 
        success: false,
        error: 'Validation failed', 
        details: validationErrors 
      });
    }

    // Check if organizer exists
    const organizer = await prisma.users.findUnique({
      where: { id: parseInt(organizerId) }
    });

    if (!organizer) {
      return res.status(400).json({ 
        success: false,
        error: 'Invalid organizer ID' 
      });
    }

    let venueId = null;
    if (venue && venue.id) {
      venueId = venue.id;
    } else if (venue && venue.name) {
      // Create new venue if provided
      const newVenue = await prisma.venues.create({
        data: {
          name: venue.name,
          street: venue.street || null,
          city: venue.city || null,
          state: venue.state || null,
          zip_code: venue.zip_code || null,
          created_by_user_id: parseInt(organizerId)
        }
      });
      venueId = newVenue.id;
    }

    // Create the event
    const newEvent = await prisma.events.create({
      data: {
        title: title.trim(),
        description: description || 'Event created via API',  // Required field
        start_date: new Date(startTime),
        end_date: endTime ? new Date(endTime) : new Date(startTime),  // Required, default to start_date
        user_id: parseInt(organizerId),
        venue_id: venueId,
        city: venue?.city || 'TBD',  // Required field
        state: venue?.state || 'TBD',  // Required field
        street: venue?.street || '',  // Required field
        zip_code: venue?.zip_code || '',  // Required field
        category: 'general',  // Required field
        target_audience: 'all',  // Required field
        fun_meter: 3,  // Required field, default value
        status: 'pending'
      },
      include: {
        user: {
          select: {
            id: true,
            first_name: true,
            last_name: true,
            company_name: true,
            email: true
          }
        },
        venue: {
          select: {
            id: true,
            name: true,
            street: true,
            city: true,
            state: true,
            zip_code: true
          }
        }
      }
    });

    console.log('Event created successfully in database:', newEvent.id);

    res.status(201).json({
      success: true,
      message: 'Event created successfully',
      event: {
        id: newEvent.id,
        title: newEvent.title,
        description: newEvent.description,
        startTime: newEvent.start_date,
        endTime: newEvent.end_date,
        organizer: newEvent.user,
        venue: newEvent.venue,
        status: newEvent.status,
        created_at: newEvent.created_at
      }
    });
  } catch (error) {
    console.error('Error creating event:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to create event',
      message: error.message 
    });
  }
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ 
    success: false,
    error: 'Endpoint not found' 
  });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ FunList Express API running on http://0.0.0.0:${PORT}`);
  console.log(`📚 Available endpoints:`);
  console.log(`   GET /health - Health check`);
  console.log(`   GET /events - Get all events`);
  console.log(`   POST /events - Create a new event`);
});

// Graceful shutdown
process.on('SIGINT', async () => {
  await prisma.$disconnect();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  await prisma.$disconnect();
  process.exit(0);
});

module.exports = app;