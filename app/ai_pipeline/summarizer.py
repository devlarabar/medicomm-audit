"""Summarize a doctor-patient conversation using Claude."""

import anthropic

from app.ai_pipeline import write_log

MODEL = "claude-sonnet-4-6"

_client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a clinical documentation assistant.
Given a doctor-patient conversation, extract and summarize the following:
- Symptoms reported by the patient
- Diagnoses or assessments made by the doctor
- Medications prescribed or discussed
- Recommendations and instructions given
- Follow-up plan

Be concise and factual. Use plain prose, not bullet points.
Keep the total summary under 150 words."""


def summarize(conversation_text: str) -> str:
    """Call Claude to produce a structured summary of the conversation."""
    message = _client.messages.create(
        model=MODEL,
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Please summarize the following conversation:\n\n{conversation_text}",
            }
        ],
    )
    result = message.content[0].text
    write_log("summary.json", {
        "model": MODEL,
        "input_tokens": message.usage.input_tokens,
        "output_tokens": message.usage.output_tokens,
    })
    return result
