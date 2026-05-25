"""
query.py
Retrieves relevant chunks from ChromaDB and generates a response via
GPT-4o-mini with player citations.
"""

import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
COLLECTION_NAME = "volleyball_wiki"
N_RESULTS = 5

client_openai = OpenAI(api_key=OPENAI_API_KEY)
client_chroma = chromadb.PersistentClient(path=CHROMA_DIR)

emb_fn = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)


def get_collection():
    return client_chroma.get_collection(
        name=COLLECTION_NAME,
        embedding_function=emb_fn
    )


def retrieve(query: str, n: int = N_RESULTS) -> list[dict]:
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=n)
    retrieved = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        retrieved.append({"text": doc, "player": meta["player"]})
    return retrieved


def build_context(chunks: list[dict]) -> str:
    lines = []
    for c in chunks:
        player_label = c["player"].replace("_", " ").title()
        lines.append(f"[{player_label}]\n{c['text']}")
    return "\n\n---\n\n".join(lines)


def answer(query: str, history: list[dict] | None = None) -> dict:
    chunks = retrieve(query)
    context = build_context(chunks)
    players_cited = list({c["player"].replace("_", " ").title() for c in chunks})

    system_prompt = f"""You are the Volleyball Masterclass AI Coach — an elite volleyball knowledge assistant
trained on the insights, techniques, and philosophies of the world's best professional players.

You answer questions using ONLY the context provided below. Be specific, practical, and cite the
player name when referencing their teaching. End every response with a bold "Key Takeaway:" line
that summarizes the core lesson in one sentence.

If the answer is not in the context, say: "I don't have specific information on that topic yet,
but you can ask about: serving, passing, setting, attacking, blocking, or mental performance."

CONTEXT:
{context}
"""

    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": query})

    response = client_openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.4,
        max_tokens=600
    )

    answer_text = response.choices[0].message.content
    return {
        "answer": answer_text,
        "players_cited": players_cited,
        "chunks_used": len(chunks)
    }


if __name__ == "__main__":
    # Quick CLI test
    q = input("Ask the Wiki: ")
    result = answer(q)
    print("\n" + result["answer"])
    print(f"\nSources: {', '.join(result['players_cited'])}")
