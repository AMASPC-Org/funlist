# Recommended Improvements to the CTO Gem Configuration

Your custom Gem configuration is fantastic and perfectly captures the 2026 Google Cloud Native standard.

Here are a few ways to improve the Gem's Instructions specifically for the `FunList.ai` frontend build and backend migration we've been working on.

## Suggested System Prompt Additions

Add these blocks to your Gem's **System Instructions** to fill a few gaps we uncovered during our backend audit:

### 1. Enforce No Tailwind/No Vite

_Why:_ We just purged Tailwind config and Vite from the FunList repository, moving everything to Next.js API Routes and standard CSS. This rule ensures the Gem yells at me (the agent) if I try to use them again.

```text
UI Constraints: You enforce Next.js App Router for all frontend applications. You strictly forbid Vite and Tailwind CSS. All styling must use vanilla CSS to maintain a premium PNW professional look.
```

### 2. Auto-Correct Legacy Assistant Code

_Why:_ Today's `assistant.ts` in the BusinessCalendar.ai repository was actually using the consumer-grade `@google/generative-ai` SDK and a hardcoded `GEMINI_API_KEY`. The rule below instructs the Gem to catch that mistake when it reviews the codebase and command agents to adapt it to Vertex AI with ADC.

```text
Code Refactoring Duty: If you encounter legacy code using `@google/generative-ai` or `GEMINI_API_KEY`, immediately instruct the agent to refactor it to `@google-cloud/vertexai` using Application Default Credentials.
```

### 3. Safety Protocols for Database

_Why:_ We are performing a Strangler Fig DB pattern (moving from PostgreSQL Drizzle to Firestore). If you copy/paste a bad prompt, an AI agent might wipe out your events table!

```text
Safety First: Remind the local system agents to never perform destructive database schema mutations without manual Operator verification and to use explicit Task Boundaries.
```

---

## Your Knowledge Files

I have generated the four template files you requested and placed them in:
**`c:\Users\USER1\ama-sites\funlist\cto_gem_knowledge`**

1. `ama-cloud-native-standards.md` -> Contains the strict workspace rules.
2. `assistant.ts` -> Written with the corrected `@google-cloud/vertexai` SDK implementation!
3. `firestore.ts` -> A schema template utilizing Firestore `GeoPoint`.
4. `events.ts` -> Demonstrates the frontend UI mapping contracts.

You can upload these straight to the Gem. Let me know when you're done, or if you want me to do anything else!
