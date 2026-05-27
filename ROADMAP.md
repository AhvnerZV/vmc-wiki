# Roadmap: v0.0 to v1.0

---

## Version Timeline

| Version | Milestone | Status |
|---|---|---|
| v0.0 | Working RAG prototype, 7 players, Streamlit | Done |
| v0.1 | LLM Wiki pipeline, React frontend, D3 graph | Done |
| v0.2 | 18+ players, expanded content, drill library | Next |
| v0.5 | FastAPI backend, hosted deployment, auth layer | Planned |
| v0.8 | Widget mode, analytics, content sync endpoint | Planned |
| v1.0 | Full pitch package, live demo URL, outreach | Planned |

---

## Phase 1 (v0.0) — Done

- 7 players in the knowledge base
- RAG pipeline: ChromaDB + OpenAI embeddings + GPT-4o-mini
- Streamlit frontend with dark court aesthetic
- Local-only, single-user, no auth

---

## Phase 2 (v0.1) — Done

- Python wiki pipeline: Writer → Evaluator → Editor (3-pass loop)
- Pydantic v2 schemas between every stage
- Player pages + auto-detected concept pages
- D3 force-directed knowledge graph
- React frontend: Chat tab, Wiki tab, Map tab
- BM25 in-browser search (no vector DB)
- Anthropic API called directly from the browser
- Static JSON output: zero server required

---

## Phase 3 (v0.2) — Next

**Goal:** Cover the full Volleyball Masterclass roster with deeper content.

- Expand to 18+ players: Ngapeth, Anderson, Zaytsev, Juantorena, and others
- Grow each player file from ~1,000 words to 2,000+ words
- Add position-specific drill libraries tied to each instructor
- Tag content by skill level (beginner, intermediate, advanced)
- Add tactical content: rotation systems, serve patterns, coverage schemes

---

## Phase 4 (v0.5) — Planned

**Goal:** Proper backend, hosted deployment, production-ready URL.

- FastAPI REST backend replaces direct browser API calls
- Hosted vector DB option (Pinecone or Qdrant) for larger corpora
- Deploy to Railway or Render with a live URL
- Session persistence across page reloads
- Query classification: technique, tactics, mindset, drill request

---

## Phase 5 (v0.8) — Planned

**Goal:** Platform integration hooks for VMC.

- iFrame-embeddable widget mode
- Auth handshake: pass a VMC subscriber token to gate access
- Admin endpoint: accepts new lesson transcripts and auto-ingests
- Analytics: query topics, player citation frequency, unanswered questions

---

## Phase 6 (v1.0) — Planned

**Goal:** Close the partnership conversation.

- 3-minute Loom demo video
- One-page PDF pitch overview
- Live hosted demo URL
- GitHub repo polished and public
- Outreach email sequence
