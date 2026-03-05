"""Scores the communication quality of a doctor-patient conversation using Claude."""

import json

import anthropic

from app.models.schemas import QualityScores

MODEL = "claude-sonnet-4-6"

_client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a clinical communication quality evaluator.
Given a doctor-patient conversation and a summary, score the doctor's communication
across four dimensions on a scale of 0 to 100.

Dimensions:
- clarity: How clear and understandable were the doctor's instructions and explanations?
- empathy: How well did the doctor acknowledge and respond to the patient's emotions?
- safety: How thoroughly did the doctor address safety-critical information?
- actionability: How actionable and specific were the doctor's recommendations?

Return a single JSON object with:
- clarity: integer 0-100
- empathy: integer 0-100
- safety: integer 0-100
- actionability: integer 0-100
- feedback: a brief overall assessment (2-3 sentences)

Return only valid JSON. No prose, no markdown."""


def score(conversation_text: str, summary: str) -> QualityScores:
    """Call Claude to score communication quality, returning a parsed model."""
    message = _client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Summary:\n{summary}\n\n"
                    f"Conversation:\n{conversation_text}"
                ),
            }
        ],
    )
    raw = json.loads(message.content[0].text)
    return QualityScores(**raw)
