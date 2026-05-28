"""
ingest.py
Reads all player .txt files from vmc_data/, chunks them, embeds them via
OpenAI, and stores them in a local ChromaDB collection.
"""

import os
import glob
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "vmc_data")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
COLLECTION_NAME = "volleyball_wiki"
CHUNK_SIZE = 400      # words per chunk
CHUNK_OVERLAP = 50    # words of overlap between chunks


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + size
        chunks.append(" ".join(words[start:end]))
        start += size - overlap
    return chunks


def ingest():
    print("Initializing ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    emb_fn = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name="text-embedding-3-small"
    )

    # Delete existing collection to allow re-ingestion
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"Deleted existing collection: {COLLECTION_NAME}")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"}
    )

    txt_files = glob.glob(os.path.join(DATA_DIR, "*.txt"))
    if not txt_files:
        print(f"No .txt files found in {DATA_DIR}")
        return

    total_chunks = 0
    for filepath in txt_files:
        player_name = os.path.splitext(os.path.basename(filepath))[0]
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)
        ids = [f"{player_name}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"player": player_name, "chunk_index": i} for i in range(len(chunks))]

        collection.add(documents=chunks, ids=ids, metadatas=metadatas)
        print(f"Ingested {len(chunks)} chunks from {player_name}")
        total_chunks += len(chunks)

    print(f"\nIngestion complete. Total chunks stored: {total_chunks}")


if __name__ == "__main__":
    ingest()
