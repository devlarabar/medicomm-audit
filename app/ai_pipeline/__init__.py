"""AI pipeline package — shared utilities for pipeline stages."""

import json
from datetime import datetime, timezone
from pathlib import Path

_LOGS_DIR = Path("logs")


def write_log(filename: str, data: object) -> None:
    """Write pipeline stage metadata to the logs/ directory as JSON.

    Logs must contain only non-PHI metadata (scores, counts, types).
    Never log conversation text, summaries, or AI-generated rewrites.
    """
    _LOGS_DIR.mkdir(exist_ok=True)
    payload = {"logged_at": datetime.now(timezone.utc).isoformat(), **data}
    (_LOGS_DIR / filename).write_text(
        json.dumps(payload, indent=2)
    )
