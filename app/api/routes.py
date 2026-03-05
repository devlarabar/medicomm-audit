"""API route definitions for the MediComm Audit pipeline."""

from fastapi import APIRouter

from app.ai_pipeline import quality_scorer, risk_analyzer, summarizer
from app.models.schemas import ConversationRequest, FullReport

router = APIRouter()


@router.post("/analyze", response_model=FullReport)
async def analyze(request: ConversationRequest) -> FullReport:
    """Run the full analysis pipeline on a doctor-patient conversation."""
    summary = summarizer.summarize(request.conversation)
    risks = risk_analyzer.analyze(request.conversation, summary)
    quality = quality_scorer.score(request.conversation, summary)
    return FullReport(summary=summary, risks=risks, quality=quality)
