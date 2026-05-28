"""
writer.py — Pass 1
Generates a structured wiki page draft from raw source content.
"""

import json
import re
from .client import create_message_with_retry
from .models import WikiPage, WikiSection

MAX_SOURCE_CHARS = 6000  # cap to prevent prompt injection via oversized files


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _sanitize_source(raw: str) -> str:
    """Trim and strip control characters from source content before injecting into prompt."""
    cleaned = raw[:MAX_SOURCE_CHARS]
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", cleaned)
    return cleaned.strip()


def _parse_json_response(raw: str) -> dict:
    """Strip markdown fences if the LLM wrapped the JSON despite instructions."""
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def write_player_page(player_name: str, raw_content: str) -> WikiPage:
    safe_content = _sanitize_source(raw_content)

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
    {{"heading": "Key Coaching Points", "content": "Actionable lessons coaches and players can apply"}},
    {{"heading": "Signature Quotes", "content": "2-3 direct quotes that capture their philosophy"}}
  ],
  "related_concepts": ["concept name 1", "concept name 2", "concept name 3"],
  "tags": ["tag1", "tag2", "tag3"]
}}

related_concepts must be general volleyball concepts. Examples: Jump Serve Mechanics,
Setter Decision Making, Mental Reset Protocols, Blocking Footprint, Serve Receive Fundamentals.

RAW CONTENT:
{safe_content}"""

    message = create_message_with_retry(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    data = _parse_json_response(message.content[0].text)

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
        f"[{player}]\n{_sanitize_source(excerpt)}"
        for player, excerpt in player_excerpts.items()
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
    {{"heading": "Players Who Excel", "content": "Which players demonstrate this best and how"}}
  ],
  "related_players": ["player name 1", "player name 2"],
  "related_concepts": ["related concept 1", "related concept 2"],
  "tags": ["tag1", "tag2"]
}}

PLAYER EXCERPTS:
{excerpts_text}"""

    message = create_message_with_retry(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    data       = _parse_json_response(message.content[0].text)
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
