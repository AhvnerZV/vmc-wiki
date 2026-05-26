"""
writer.py — Pass 1
Generates a structured wiki page draft from raw source content.
Uses the Anthropic API.
"""

import json
import re
import anthropic
from .models import WikiPage, WikiSection

client = anthropic.Anthropic()


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def write_player_page(player_name: str, raw_content: str) -> WikiPage:
    prompt = f"""You are a volleyball knowledge editor. Given the raw coaching notes below for {player_name},
write a structured wiki page. Return ONLY valid JSON matching this exact schema — no markdown fences, no preamble:

{{
  "title": "Full player name",
  "position": "Position",
  "nationality": "Nationality",
  "summary": "2-3 sentence overview of this player's elite strengths and coaching value",
  "sections": [
    {{"heading": "Overview", "content": "3-4 sentences on who they are and why they matter"}},
    {{"heading": "Technique", "content": "Detailed breakdown of their core technical skills"}},
    {{"heading": "Mindset & Philosophy", "content": "Their mental approach and coaching philosophy"}},
    {{"heading": "Key Coaching Points", "content": "Bullet-style actionable lessons coaches and players can apply"}},
    {{"heading": "Signature Quotes", "content": "2-3 direct quotes that capture their philosophy"}}
  ],
  "related_concepts": ["concept name 1", "concept name 2", "concept name 3"],
  "tags": ["tag1", "tag2", "tag3"]
}}

related_concepts must be general volleyball concepts this player's content touches on.
Examples: Jump Serve Mechanics, Setter Decision Making, Mental Reset Protocols,
Blocking Footprint, Back Row Attack, Serve Receive Fundamentals, Approach Timing.

RAW CONTENT:
{raw_content}"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    data = json.loads(raw)

    return WikiPage(
        id=slugify(data["title"]),
        title=data["title"],
        type="player",
        position=data.get("position", ""),
        nationality=data.get("nationality", ""),
        summary=data["summary"],
        sections=[WikiSection(**s) for s in data["sections"]],
        related=data.get("related_concepts", []),
        tags=data.get("tags", [])
    )


def write_concept_page(concept_name: str, player_excerpts: dict[str, str]) -> WikiPage:
    excerpts_text = "\n\n".join(
        f"[{player}]\n{excerpt}" for player, excerpt in player_excerpts.items()
    )

    prompt = f"""You are a volleyball knowledge editor. Write a concept wiki page for "{concept_name}".
This concept appears across multiple elite players' coaching content. Synthesize their approaches.
Return ONLY valid JSON — no markdown fences, no preamble:

{{
  "title": "{concept_name}",
  "summary": "2-3 sentence definition of this concept and why it matters at the elite level",
  "sections": [
    {{"heading": "What It Is", "content": "Clear definition and why this concept is fundamental"}},
    {{"heading": "How The Elite Do It", "content": "Specific technical details drawn from the players below"}},
    {{"heading": "Common Mistakes", "content": "What separates elite execution from average execution"}},
    {{"heading": "Drills & Practice", "content": "Concrete ways to train this concept"}},
    {{"heading": "Players Who Excel", "content": "Which players in our knowledge base demonstrate this best and how"}}
  ],
  "related_players": ["player name 1", "player name 2"],
  "related_concepts": ["related concept 1", "related concept 2"],
  "tags": ["tag1", "tag2"]
}}

PLAYER EXCERPTS:
{excerpts_text}"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    data = json.loads(raw)

    all_related = data.get("related_players", []) + data.get("related_concepts", [])

    return WikiPage(
        id=slugify(data["title"]),
        title=data["title"],
        type="concept",
        summary=data["summary"],
        sections=[WikiSection(**s) for s in data["sections"]],
        related=all_related,
        tags=data.get("tags", [])
    )
