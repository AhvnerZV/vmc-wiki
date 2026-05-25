# Volleyball Masterclass Wiki LLM

**Version 0.0** — Working proof-of-concept

A RAG-powered AI coaching assistant trained on the techniques, tactics, and philosophy of elite professional volleyball players. Built as a partnership pitch for Volleyball Masterclass.

---

## What It Does

Ask any question about volleyball technique, tactics, serving, passing, setting, attacking, blocking, or mental performance. The system retrieves the most relevant knowledge from the player library and generates a specific, cited response — not a generic answer.

**Players in the knowledge base (v0.0):**
- Wilfredo León — Outside Hitter
- Antoine Brizard — Setter
- Jenia Grebennikov — Libero
- TJ DeFalco — Opposite Hitter
- Nimir Abdel-Aziz — Opposite Hitter
- Luciano De Cecco — Setter
- Reid Hall — Coach / Clinician

---

## Tech Stack

| Layer | Tool |
|---|---|
| Knowledge base | Plain-text player files (`vmc_data/`) |
| Embeddings | OpenAI `text-embedding-3-small` |
| Vector store | ChromaDB (local persistent) |
| LLM | GPT-4o-mini |
| Frontend | Streamlit |

---

## Quick Start

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/vmc-wiki.git
cd vmc-wiki
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set your OpenAI API key**
```bash
cp .env.example .env
# Edit .env and add your key
```

**4. Build the knowledge base**
```bash
python src/ingest.py
```

**5. Launch the app**
```bash
streamlit run app.py
```

Opens at `http://localhost:8501`.

---

## Project Structure

```
vmc-wiki/
├── vmc_data/               Player knowledge base files (.txt)
│   ├── wilfredo_leon.txt
│   ├── antoine_brizard.txt
│   ├── jenia_grebennikov.txt
│   ├── tj_defalco.txt
│   ├── nimir_abdel_aziz.txt
│   ├── luciano_de_cecco.txt
│   └── reid_hall.txt
├── src/
│   ├── ingest.py           Chunking, embedding, ChromaDB ingestion
│   └── query.py            Retrieval and GPT-4o-mini response generation
├── app.py                  Streamlit UI
├── requirements.txt
├── .env.example
└── ROADMAP.md
```

---

## The Pitch

Volleyball Masterclass has the brand and the athletes. The platform lacks an interactive layer. Members watch a masterclass, get inspired, and then have nowhere to go with their questions. This Wiki LLM is that layer — embedded directly inside the platform, it transforms passive watching into active coaching dialogue.

See `ROADMAP.md` for the full build plan toward v1.0.

---

## Status

`v0.0` — functional prototype. All core components working: ingestion, retrieval, response generation, Streamlit UI. Ready for Loom demo recording.
