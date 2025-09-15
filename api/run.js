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
      
      if (start) {
        const startDate = new Date(start);
        if (isNaN(startDate.getTime())) {
          return res.status(400).json({
            success: false,
            error: 'Invalid start date format. Use YYYY-MM-DD'
          });
        }
        whereClause.start_date.gte = startDate;
      }
      
      if (end) {
        const endDate = new Date(end);
        if (isNaN(endDate.getTime())) {
          return res.status(400).json({
            success: false,
            error: 'Invalid end date format. Use YYYY-MM-DD'
          });
        }
        // Set to end of day
        endDate.setHours(23, 59, 59, 999);
        whereClause.start_date.lte = endDate;
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
            city: {
              contains: location,
              mode: 'insensitive'
            }
          }
        },
        {
          venue: {
            state: {
              contains: location,
              mode: 'insensitive'
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