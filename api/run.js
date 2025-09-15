// Simple API runner with better port handling
require('dotenv').config();

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

// GET /events - returns all events (with fallback for missing tables)
app.get('/events', async (req, res) => {
  try {
    console.log('GET /events requested');
    
    // Since database tables aren't ready, return mock data for demonstration
    const mockEvents = [
      {
        id: 1,
        title: "Sample Community Event",
        description: "A great community gathering",
        startTime: new Date('2025-09-20T18:00:00Z'),
        endTime: new Date('2025-09-20T21:00:00Z'),
        location: "Community Center",
        city: "Seattle",
        state: "WA",
        category: "Community",
        funalyticsScore: {
          fun_rating: 4,
          fun_meter: 4
        },
        organizer: {
          id: 1,
          first_name: "John",
          last_name: "Doe",
          company_name: "Community Events Inc",
          email: "john@example.com"
        },
        venue: {
          id: 1,
          name: "Downtown Community Center",
          street: "123 Main St",
          city: "Seattle",
          state: "WA",
          zip_code: "98101",
          venue_type: {
            name: "Community Center",
            category: "Public"
          }
        },
        status: "approved",
        created_at: new Date()
      }
    ];

    console.log(`Returning ${mockEvents.length} mock events (database tables not yet available)`);

    res.json({
      success: true,
      count: mockEvents.length,
      events: mockEvents,
      note: "Mock data - database tables will be connected once Flask migrations are complete"
    });
  } catch (error) {
    console.error('Error in events endpoint:', error);
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

    // Since database tables aren't ready, simulate successful creation
    const mockEvent = {
      id: Date.now(), // Use timestamp as ID for demonstration
      title: title.trim(),
      description: description || null,
      startTime: new Date(startTime),
      endTime: endTime ? new Date(endTime) : null,
      organizer: {
        id: parseInt(organizerId),
        first_name: "Mock",
        last_name: "Organizer",
        company_name: "Event Company",
        email: "organizer@example.com"
      },
      venue: venue || null,
      status: 'pending',
      created_at: new Date()
    };

    console.log('Mock event created successfully:', mockEvent.id);

    res.status(201).json({
      success: true,
      message: 'Event created successfully (mock response)',
      event: mockEvent,
      note: "Mock response - will connect to database once Flask migrations are complete"
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