import 'dotenv/config';
import express from 'express';
import type { Request, Response } from 'express'; // The Fix: Type-Only Import
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();
const app = express();
const port = process.env.PORT || 3001; // Using 3001 to avoid frontend conflicts

app.use(express.json());

// 1. Health Check Route
app.get('/', (req: Request, res: Response) => {
  res.json({
    status: 'ok',
    message: 'FunList API is running on the Golden Path (TypeScript)!'
  });
});

// 2. Events Route (Test your Database Connection)
app.get('/events', async (req: Request, res: Response) => {
  try {
    // This attempts to fetch events from your new Prisma Client
    const events = await prisma.event.findMany();
    res.json(events);
  } catch (error) {
    console.error('Database Error:', error);
    // If the table doesn't exist yet, we return a helpful error
    res.status(500).json({
      error: 'Failed to fetch events.',
      details: String(error)
    });
  }
});

app.listen(port, () => {
  console.log(`🚀 Server is running on http://localhost:${port}`);
});