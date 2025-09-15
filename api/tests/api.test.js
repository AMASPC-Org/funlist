const request = require('supertest');
const app = require('../run.js');

describe('FunList API Endpoints', () => {
  describe('GET /health', () => {
    it('should return health check with status OK', async () => {
      const response = await request(app)
        .get('/health')
        .expect(200);

      expect(response.body).toMatchObject({
        status: 'OK',
        message: 'FunList API is running',
        port: 3001
      });
      expect(response.body.timestamp).toBeDefined();
    });
  });

  describe('GET /events', () => {
    it('should return events list with proper structure', async () => {
      const response = await request(app)
        .get('/events')
        .expect(200);

      expect(response.body).toMatchObject({
        success: true,
        count: expect.any(Number),
        events: expect.any(Array)
      });

      // Verify event structure if events exist
      if (response.body.events.length > 0) {
        const event = response.body.events[0];
        expect(event).toMatchObject({
          id: expect.any(Number),
          title: expect.any(String),
          startTime: expect.any(String),
          funalyticsScore: {
            fun_rating: expect.any(Number),
            fun_meter: expect.any(Number)
          },
          organizer: expect.objectContaining({
            id: expect.any(Number),
          }),
          status: expect.any(String),
        });
      }
    });

    it('should filter events by title', async () => {
      const response = await request(app)
        .get('/events?title=festival')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.count).toBeGreaterThan(0);
      
      // Check that returned events contain "festival" in title (case-insensitive)
      response.body.events.forEach(event => {
        expect(event.title.toLowerCase()).toContain('festival');
      });
    });

    it('should filter events by location', async () => {
      const response = await request(app)
        .get('/events?location=seattle')
        .expect(200);

      expect(response.body.success).toBe(true);
      
      // Check that returned events are in Seattle
      response.body.events.forEach(event => {
        const location = (event.city + ' ' + event.state + ' ' + 
                         (event.venue?.city || '') + ' ' + (event.venue?.state || '')).toLowerCase();
        expect(location).toContain('seattle');
      });
    });

    it('should filter events by date range', async () => {
      const response = await request(app)
        .get('/events?start=2025-04-01&end=2025-04-30')
        .expect(200);

      expect(response.body.success).toBe(true);
      
      // Check that returned events are within April 2025
      response.body.events.forEach(event => {
        const eventDate = new Date(event.startTime);
        expect(eventDate.getFullYear()).toBe(2025);
        expect(eventDate.getMonth()).toBe(3); // April is month 3 (0-indexed)
      });
    });

    it('should validate date format and return 400 for invalid dates', async () => {
      const response = await request(app)
        .get('/events?start=invalid-date')
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toContain('Invalid start date format');
    });

    it('should support combined filters', async () => {
      const response = await request(app)
        .get('/events?title=festival&location=olympia')
        .expect(200);

      expect(response.body.success).toBe(true);
      
      // Check that events match both filters
      response.body.events.forEach(event => {
        expect(event.title.toLowerCase()).toContain('festival');
        const location = (event.city + ' ' + event.state + ' ' + 
                         (event.venue?.city || '') + ' ' + (event.venue?.state || '')).toLowerCase();
        expect(location).toContain('olympia');
      });
    });
  });

  describe('POST /events', () => {
    const validEventData = {
      title: 'Test Event',
      description: 'Test event description',
      startTime: '2025-12-15T19:00:00Z',
      endTime: '2025-12-15T22:00:00Z',
      organizerId: '1',
      venue: {
        name: 'Test Venue',
        city: 'Seattle',
        state: 'WA'
      }
    };

    it('should create event with valid data', async () => {
      const response = await request(app)
        .post('/events')
        .send(validEventData)
        .expect(201);

      expect(response.body).toMatchObject({
        success: true,
        message: expect.stringContaining('created successfully'),
        event: expect.objectContaining({
          id: expect.any(Number),
          title: validEventData.title,
          description: validEventData.description,
          organizer: expect.objectContaining({
            id: parseInt(validEventData.organizerId)
          }),
          status: 'pending',
          created_at: expect.any(String)
        })
      });
    });

    it('should validate required fields', async () => {
      const invalidData = {
        title: '',
        startTime: '',
        organizerId: ''
      };

      const response = await request(app)
        .post('/events')
        .send(invalidData)
        .expect(400);

      expect(response.body).toMatchObject({
        success: false,
        error: 'Validation failed',
        details: expect.arrayContaining([
          'Title is required',
          'Start time is required',
          'Organizer ID is required'
        ])
      });
    });

    it('should validate start time before end time', async () => {
      const invalidTimeData = {
        title: 'Test Event',
        startTime: '2025-12-15T22:00:00Z',
        endTime: '2025-12-15T19:00:00Z',
        organizerId: '1'
      };

      const response = await request(app)
        .post('/events')
        .send(invalidTimeData)
        .expect(400);

      expect(response.body.details).toContain('Start time must be before end time');
    });

    it('should handle missing required fields', async () => {
      const response = await request(app)
        .post('/events')
        .send({})
        .expect(400);

      expect(response.body).toMatchObject({
        success: false,
        error: 'Validation failed'
      });
    });
  });

  describe('Error Handling', () => {
    it('should return 404 for unknown endpoints', async () => {
      const response = await request(app)
        .get('/unknown')
        .expect(404);

      expect(response.body).toMatchObject({
        success: false,
        error: 'Endpoint not found'
      });
    });

    it('should handle malformed JSON in POST requests', async () => {
      const response = await request(app)
        .post('/events')
        .set('Content-Type', 'application/json')
        .send('invalid json')
        .expect(400);
    });
  });

  describe('CORS Headers', () => {
    it('should include CORS headers in responses', async () => {
      const response = await request(app)
        .get('/health')
        .expect(200);

      expect(response.headers['access-control-allow-origin']).toBeDefined();
      expect(response.headers['access-control-allow-methods']).toBeDefined();
      expect(response.headers['access-control-allow-headers']).toBeDefined();
    });

    it('should handle OPTIONS requests', async () => {
      await request(app)
        .options('/events')
        .expect(200);
    });
  });
});