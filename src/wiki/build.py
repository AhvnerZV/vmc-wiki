"""
build.py
Orchestrates the full Writer -> Evaluator -> Editor pipeline.
Generates player pages, detects concepts, builds graph, outputs wiki_data.json.
"""

import os
import json
import glob
from datetime import datetime, timezone
from collections import defaultdict

from .models import WikiData
from .writer import write_player_page, write_concept_page, slugify
from .evaluator import evaluate_page
from .editor import edit_page
from .graph import build_graph

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "vmc_data")
OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "frontend", "src", "data", "wiki_data.json"
)

KNOWN_CONCEPTS = [
    "Jump Serve Mechanics",
    "Serve Receive Fundamentals",
    "Setter Decision Making",
    "Blocking Footprint",
    "Approach Timing",
    "Back Row Attack",
    "Mental Reset Protocols",
    "Platform Mechanics",
    "Attack Angle Selection",
    "Reading the Block",
]


def run_three_pass(page, source=""):
    print(f"    Evaluating...")
    evaluation = evaluate_page(page, source)
    print(f"    Score: {evaluation.score}/5")
    if evaluation.score < 4:
        print(f"    Editing: {evaluation.improvements}")
        page = edit_page(page, evaluation)
    else:
        page.quality_score = evaluation.score
    return page


def build():
    print("\n=== VMC Wiki Build Pipeline ===\n")

    txt_files = glob.glob(os.path.join(DATA_DIR, "*.txt"))
    if not txt_files:
        print(f"No .txt files found in {DATA_DIR}")
        return

    player_pages = []
    concept_mentions: dict[str, dict[str, str]] = defaultdict(dict)

    for filepath in sorted(txt_files):
        player_name = os.path.splitext(os.path.basename(filepath))[0].replace("_", " ").title()
        print(f"[Player] {player_name}")

        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()

        print(f"  Writing draft...")
        page = write_player_page(player_name, raw)

        page = run_three_pass(page, raw)
        player_pages.append(page)
        print(f"  Done. ID: {page.id}")

        for concept in KNOWN_CONCEPTS:
            concept_lower = concept.lower()
            if any(concept_lower in s.content.lower() for s in page.sections):
                excerpt = raw[:800]
                concept_mentions[concept][page.title] = excerpt

    print(f"\nGenerated {len(player_pages)} player pages.\n")

    concept_pages = []
    for concept_name, excerpts in concept_mentions.items():
        if len(excerpts) < 2:
            continue
        print(f"[Concept] {concept_name} (mentioned by {len(excerpts)} players)")
        print(f"  Writing draft...")
        page = write_concept_page(concept_name, excerpts)
        page = run_three_pass(page)
        concept_pages.append(page)
        print(f"  Done. ID: {page.id}")

    print(f"\nGenerated {len(concept_pages)} concept pages.\n")

    print("Building graph...")
    graph = build_graph(player_pages, concept_pages)
    print(f"Graph: {len(graph.nodes)} nodes, {len(graph.links)} links\n")

    wiki_data = WikiData(
        players=player_pages,
        concepts=concept_pages,
        graph=graph,
        built_at=datetime.now(timezone.utc).isoformat()
    )

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(wiki_data.model_dump(), f, indent=2)

    print(f"wiki_data.json written to: {OUTPUT_PATH}")
    print(f"\nBuild complete.")
    print(f"  Players: {len(player_pages)}")
    print(f"  Concepts: {len(concept_pages)}")
    print(f"  Graph nodes: {len(graph.nodes)}")
    print(f"  Graph links: {len(graph.links)}")
