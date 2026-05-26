"""
evaluator.py — Pass 2
Scores a wiki page draft 1-5 on coverage, clarity, and structure.
"""

import json
import anthropic
from .models import WikiPage, EvaluationResult

client = anthropic.Anthropic()


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

Score 5 = publication ready. Score 3 = needs work. Score 1 = major rewrite needed.
List improvements only if score < 4. Max 3 improvements.

PAGE TITLE: {page.title}
SUMMARY: {page.summary}

SECTIONS:
{sections_text}"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    data = json.loads(raw)
    return EvaluationResult(**data)
