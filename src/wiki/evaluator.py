"""
evaluator.py — Pass 2
Scores a wiki page draft 1-5 on coverage, clarity, and structure.
"""

import re
import json
from .client import create_message_with_retry
from .models import WikiPage, EvaluationResult


def _parse_json_response(raw: str) -> dict:
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def evaluate_page(page: WikiPage, source_content: str = "") -> EvaluationResult:
    sections_text = "\n\n".join(
        f"## {s.heading}\n{s.content}" for s in page.sections
    )

    prompt = f"""You are a wiki quality evaluator. Score this volleyball wiki page 1-5 on:
- Coverage: Does it capture the most important technical information?
- Clarity: Is it specific and actionable, not vague?
- Structure: Does it flow logically and use consistent formatting?

Return ONLY valid JSON — no markdown, no preamble:
{{
  "score": <integer 1-5>,
  "improvements": ["specific improvement 1", "specific improvement 2"]
}}

Score 5 = publication ready. Score 4 = good, minor polish only. Score 3 = needs work.
List improvements only if score < 4. Max 3 improvements.

PAGE TITLE: {page.title}
SUMMARY: {page.summary}

SECTIONS:
{sections_text}"""

    message = create_message_with_retry(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )

    data = _parse_json_response(message.content[0].text)
    return EvaluationResult(**data)
