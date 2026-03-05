"""Detects clinical communication risks in a conversation using Claude."""

import json

import anthropic

from app.ai_pipeline import write_log
from app.ai_pipeline.parser import parse
from app.models.schemas import RiskAnalysis

MODEL = "claude-sonnet-4-6"

_client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a clinical communication safety reviewer.
Given a doctor-patient conversation and a summary, identify any communication risks.

Risk categories to check for:
- unclear_instructions: Instructions that are vague or could be misunderstood
- dismissed_symptoms: Patient concerns that were downplayed or ignored
- missing_follow_up: No follow-up plan was established when one was needed
- ambiguous_advice: Advice that could be interpreted in conflicting ways
- early_medication_stop: Patient indicates they may stop medication early without guidance

Return a JSON array of risk objects. Each object must have:
- risk_types: array of applicable risk category strings
- severity: "low", "medium", or "high"
- explanation: brief explanation of the risk
- message_reference: 1-based index of the message where the risk occurs
- safer_rewrite: a safer alternative phrasing for the problematic message

If no risks are found, return an empty array: []

Return only valid JSON. No prose, no markdown."""


def analyze(conversation_text: str, summary: str) -> list[RiskAnalysis]:
    """Call Claude to identify risks in the conversation, returning parsed models."""
    messages = parse(conversation_text)
    numbered = "\n".join(
        f"[{m['index']}] {m['speaker']}: {m['text']}" for m in messages
    )
    message = _client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Summary:\n{summary}\n\n"
                    f"Conversation (each line prefixed with its message number):\n{numbered}"
                ),
            }
        ],
    )
    raw = json.loads(message.content[0].text)
    risks = [RiskAnalysis(**item) for item in raw]
    write_log("risk.json", {
        "model": MODEL,
        "input_tokens": message.usage.input_tokens,
        "output_tokens": message.usage.output_tokens,
        "risk_count": len(risks),
        "severities": [r.severity for r in risks],
        "risk_types": [r.risk_types for r in risks],
    })
    return risks
