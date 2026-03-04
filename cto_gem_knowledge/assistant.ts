import { randomUUID } from "crypto";
import { VertexAI, HarmCategory, HarmBlockThreshold } from "@google-cloud/vertexai";
import type { EventSearchFilters } from "../shared/event.types.js";
import type { AssistantResponse, ChatMessage } from "../shared/assistant.types.js";
import { searchEvents } from "./eventSearch.js";

// AI Configuration using Vertex AI and Application Default Credentials
// A key feature of standard 2026 Google Cloud Architecture
const PROJECT_ID = process.env.GOOGLE_CLOUD_PROJECT || "ama-enterprise-production";
const LOCATION = "us-central1"; 
const MODEL = "gemini-3.1-pro"; // Enforced auto-updating model alias

// Initialize Vertex AI with ADC (Requires no API keys)
const vertexAI = new VertexAI({ project: PROJECT_ID, location: LOCATION });
const generativeModel = vertexAI.getGenerativeModel({
  model: MODEL,
  generationConfig: {
    maxOutputTokens: 600,
    temperature: 0.2,
  },
  safetySettings: [
    {
      category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
      threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    },
  ],
});

export async function buildAssistantResponse(userMessage: string): Promise<AssistantResponse> {
  try {
    const filters = await extractSearchFilters(userMessage);

    const responseContent = "I am searching the A2A Mesh for your events..."; // dynamic text implementation omitted for brevity

    const assistantMessage: ChatMessage = {
      id: randomUUID(),
      role: "assistant",
      content: responseContent,
      timestamp: new Date().toISOString(),
    };

    const events = await searchEvents(filters, 3).catch(() => []);

    return { message: assistantMessage, filters, events };
  } catch (error) {
    console.error("Error building assistant response with VertexAI:", error);
    return fallbackResponse();
  }
}

async function extractSearchFilters(userText: string): Promise<EventSearchFilters> {
  const prompt = `
Extract event search criteria from this user request: "${userText}"
Return ONLY a valid JSON object with optional fields:
{
  "cities": ["City1"],
  "state": "WA",
  "dateRange": {"start": "2026-01-01", "end": "2026-01-31"},
  "industries": ["real-estate"],
  "keywords": ["networking"]
}
Today is ${new Date().toISOString().split('T')[0]}.
`;

  try {
    const result = await generativeModel.generateContent({
      contents: [{ role: 'user', parts: [{ text: prompt }] }],
    });
    
    if (result.response.candidates && result.response.candidates.length > 0) {
      const responseText = result.response.candidates[0].content.parts[0].text;
      if (responseText) {
        // Strip markdown blocks if they exist
        const parsed = JSON.parse(responseText.replace(/\`\`\`json/g, '').replace(/\`\`\`/g, '').trim());
        return parsed as EventSearchFilters;
      }
    }
    return {};
  } catch (err) {
    console.warn("Failed to extract LLM filters via VertexAI:", err);
    return {};
  }
}

function fallbackResponse(): AssistantResponse {
  return {
    message: {
      id: randomUUID(),
      role: "assistant",
      content: "I'm having trouble connecting to Vertex AI via ADC right now. Please try again.",
      timestamp: new Date().toISOString(),
    },
    filters: {}
  };
}
