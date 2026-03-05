"""Parses raw conversation text into a list of indexed messages."""

import re


def parse(conversation_text: str) -> list[dict]:
    """Split a conversation into a list of {index, speaker, text} dicts.

    Expects lines in the format "Speaker: message text". Lines that don't
    match are appended to the previous message's text.
    """
    pattern = re.compile(r"^([^:]+):\s*(.+)$")
    messages = []

    for line in conversation_text.splitlines():
        line = line.strip()
        if not line:
            continue

        match = pattern.match(line)
        if match:
            messages.append({
                "index": len(messages) + 1,
                "speaker": match.group(1).strip(),
                "text": match.group(2).strip(),
            })
        elif messages:
            messages[-1]["text"] += " " + line

    return messages
