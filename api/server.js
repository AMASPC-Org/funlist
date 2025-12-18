require('dotenv').config();

const express = require('express');
const { PrismaClient } = require('./generated/prisma');

const app = express();
const prisma = new PrismaClient();

const PORT = process.env.PORT || 3001;

// Middleware
app.use(express.json());

// CORS middleware for the Flask origin
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', 'http://localhost:8080');
  res.header('Access-Control-Allow-Origin', 'https://workspace.AMASPC.repl.co');
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
  res.json({ status: 'OK', message: 'FunList API is running' });
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
    const page = parseInt(req.query.page) || 1;
    const limit = Math.min(parseInt(req.query.limit) || 20, 100);
    const offset = (page - 1) * limit;

    const events = await prisma.event.findMany({
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
            venue_type: {
              select: {
                name: true,
                category: true
              }
            }
          }
        }
      },
      orderBy: {
        created_at: 'desc'
      }
    });

    const totalEvents = await prisma.event.count();
    
    res.json({
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
    res.status(500).json({ error: 'Internal server error' });
  }
});

// POST /events - allows an organizer to submit a new event
app.post('/events', async (req, res) => {
  try {
    const { title, description, startTime, endTime, venue, organizerId } = req.body;
    
    // Validate input
    const validationErrors = validateEventData({ title, startTime, endTime, organizerId });
    if (validationErrors.length > 0) {
      return res.status(400).json({ 
        error: 'Validation failed', 
        details: validationErrors 
      });
    }

    // Check if organizer exists
    const organizer = await prisma.user.findUnique({
      where: { id: parseInt(organizerId) }
    });

    if (!organizer) {
      return res.status(400).json({ error: 'Invalid organizer ID' });
    }

    let venueId = null;
    if (venue && venue.id) {
      venueId = venue.id;
    } else if (venue && venue.name) {
      // Create new venue if provided
      const newVenue = await prisma.venue.create({
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
    const newEvent = await prisma.event.create({
      data: {
        title: title.trim(),
        description: description || null,
        start_date: new Date(startTime),
        end_date: endTime ? new Date(endTime) : null,
        user_id: parseInt(organizerId),
        venue_id: venueId,
        city: venue?.city || null,
        state: venue?.state || null,
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

    res.status(201).json({
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
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
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

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Express API server running on http://0.0.0.0:${PORT}`);
  console.log(`📚 Available endpoints:`);
  console.log(`   GET /health - Health check`);
  console.log(`   GET /events - Get all events with pagination`);
  console.log(`   POST /events - Create a new event`);
});

module.exports = app;
