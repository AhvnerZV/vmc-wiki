"""
editor.py — Pass 3
Applies improvements to a wiki page draft based on evaluator feedback.
"""

import re
import json
from .client import create_message_with_retry
from .models import WikiPage, WikiSection, EvaluationResult


def _parse_json_response(raw: str) -> dict:
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def edit_page(page: WikiPage, evaluation: EvaluationResult) -> WikiPage:
    if evaluation.score >= 4:
        page.quality_score = evaluation.score
        return page

    sections_json     = [{"heading": s.heading, "content": s.content} for s in page.sections]
    improvements_text = "\n".join(f"- {i}" for i in evaluation.improvements)

    prompt = f"""You are a wiki editor. Improve this volleyball wiki page based on the feedback below.
Return ONLY valid JSON with the improved content — no markdown fences, no preamble:

{{
  "summary": "improved summary if needed, otherwise keep original",
  "sections": [
    {{"heading": "heading", "content": "improved content"}}
  ]
}}

Keep all existing section headings. Only improve the content.

IMPROVEMENTS NEEDED:
{improvements_text}

CURRENT SUMMARY: {page.summary}

CURRENT SECTIONS:
{json.dumps(sections_json, indent=2)}"""

    message = create_message_with_retry(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    data          = _parse_json_response(message.content[0].text)
    page.summary  = data.get("summary", page.summary)
    page.sections = [WikiSection(**s) for s in data["sections"]]
    page.quality_score = evaluation.score
    return page
