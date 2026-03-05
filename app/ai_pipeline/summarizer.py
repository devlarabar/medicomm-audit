"""Summarize a doctor-patient conversation using Claude."""

import anthropic

MODEL = "claude-sonnet-4-6"

_client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a clinical documentation assistant.
Given a doctor-patient conversation, extract and summarize the following:
- Symptoms reported by the patient
- Diagnoses or assessments made by the doctor
- Medications prescribed or discussed
- Recommendations and instructions given
- Follow-up plan

Be concise and factual. Use plain prose, not bullet points."""


def summarize(conversation_text: str) -> str:
    """Call Claude to produce a structured summary of the conversation."""
    message = _client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Please summarize the following conversation:\n\n{conversation_text}",
            }
        ],
    )
    return message.content[0].text
