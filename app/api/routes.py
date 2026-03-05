"""API route definitions for the Medicomm Audit pipeline."""

from fastapi import APIRouter

from app.ai_pipeline import quality_scorer, risk_analyzer, summarizer
from app.models.schemas import ConversationRequest, FullReport

router = APIRouter()

_analysis_history: list[FullReport] = []


@router.post("/analyze", response_model=FullReport)
async def analyze(request: ConversationRequest) -> FullReport:
    """Run the full analysis pipeline on a doctor-patient conversation."""
    summary = summarizer.summarize(request.conversation)
    risks = risk_analyzer.analyze(request.conversation, summary)
    quality = quality_scorer.score(request.conversation, summary)
    report = FullReport(summary=summary, risks=risks, quality=quality)
    _analysis_history.append(report)
    return report


@router.get("/metrics")
async def metrics() -> dict:
    """Return aggregate quality scores across all analysed conversations."""
    total = len(_analysis_history)
    if total == 0:
        return {"total_conversations": 0, "average_scores": None}

    score_fields = ["clarity", "empathy", "safety", "actionability"]
    averages = {
        field: round(
            sum(r.quality.model_dump()[field] for r in _analysis_history) / total, 1
        )
        for field in score_fields
    }
    return {"total_conversations": total, "average_scores": averages}
