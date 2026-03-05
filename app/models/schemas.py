"""Pydantic schemas for pipeline request and response types."""

from typing import Literal

from pydantic import BaseModel, Field


class ConversationRequest(BaseModel):
    """Incoming request containing the raw doctor-patient conversation text."""

    conversation: str


class RiskAnalysis(BaseModel):
    """A single identified risk in the conversation, with location and rewrite."""

    risk_types: list[
        Literal[
            "unclear_instructions",
            "dismissed_symptoms",
            "missing_follow_up",
            "ambiguous_advice",
            "early_medication_stop",
        ]
    ]
    severity: Literal["low", "medium", "high"]
    explanation: str
    message_reference: int = Field(
        description="1-based index of the conversation message where the risk occurs."
    )
    safer_rewrite: str


class QualityScores(BaseModel):
    """Communication quality scores (0-100) across four dimensions."""

    clarity: int
    empathy: int
    safety: int
    actionability: int
    feedback: str


class FullReport(BaseModel):
    """Assembled output of the full analysis pipeline."""

    summary: str
    risks: list[RiskAnalysis]
    quality: QualityScores
