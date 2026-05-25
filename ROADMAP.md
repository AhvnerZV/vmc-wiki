# Roadmap: v0.0 to v1.0

This document outlines the full build plan for taking the Volleyball Wiki LLM
from a working proof-of-concept (v0.0) to a production-ready partnership demo (v1.0).

---

## Current State (v0.0)

- 7 players in the knowledge base
- RAG pipeline: ChromaDB + OpenAI embeddings + GPT-4o-mini
- Streamlit frontend with dark court aesthetic
- Local-only, single-user, no auth
- Knowledge base is manually written text files

---

## Phase 1. Knowledge Base Expansion

**Goal:** Cover the full Volleyball Masterclass roster (18+ players) with deeper content.

- Add remaining VMC players: Earvin Ngapeth, Matthew Anderson, Ivan Zaytsev, Osmany Juantorena, and others
- Expand each player file from ~800 words to 1,500+ words
- Add tactical content: rotation strategies, system play (5-1 vs 6-2), serve patterns
- Add position-specific drills tied to each instructor
- Tag content by skill level (beginner, intermediate, advanced) for filtered retrieval

---

## Phase 2. Backend Upgrade

**Goal:** Replace the local Streamlit setup with a proper API backend.

- Migrate from Streamlit to a FastAPI REST backend
- Replace local ChromaDB with a hosted vector DB (Pinecone or Qdrant)
- Add a session management layer so conversation history persists across page reloads
- Implement a query router: classify each question (technique, tactics, mindset, drill request) and adjust retrieval strategy per category
- Add source confidence scoring so the UI can display how closely the answer matched the retrieved content

---

## Phase 3. Frontend Rebuild

**Goal:** Replace Streamlit with a production-quality React frontend that matches the VMC brand.

- React + Vite + Tailwind
- Replicate VMC design system: dark background (#0C0D12), gold accent (#FFD100), Barlow Condensed typography
- Full 18-player sidebar with position filters (OH, OPP, S, MB, L)
- Player profile cards: click a player to pre-load their context window
- Message threading with citations rendered as player avatar tags
- Mobile responsive layout
- Framer Motion animations: message reveal, loading state, sidebar transitions

---

## Phase 4. VMC Integration Layer

**Goal:** Build the hooks needed to embed this inside an existing platform.

- iFrame-embeddable widget mode (standalone chat component)
- Auth handshake: pass a VMC subscriber token to gate access
- Content sync: an admin endpoint that accepts new lesson transcripts and auto-ingests them into the vector DB
- Analytics: log query topics, player citation frequency, unanswered questions (for content gap analysis)

---

## Phase 5. Pitch Deliverables

**Goal:** Package everything needed to close the partnership conversation.

- 3-minute Loom demo video
- One-page PDF pitch overview (problem, solution, integration path, pricing model)
- Live hosted demo URL (deployed on Railway or Render)
- GitHub repo polished and public
- Outreach email sequence (initial pitch, follow-up, final nudge)

---

## Version Timeline (Target)

| Version | Milestone | Target |
|---|---|---|
| v0.0 | Working prototype, 7 players, Streamlit | Done |
| v0.1 | 18 players, expanded content, drill library | Week 2 |
| v0.2 | FastAPI backend, hosted vector DB | Week 3 |
| v0.5 | React frontend, production UI | Week 4 |
| v0.8 | Widget mode, auth layer, analytics | Week 5 |
| v1.0 | Full pitch package, live demo, outreach begins | Week 6 |
