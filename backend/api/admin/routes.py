from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.agents.orchestrator import orchestrator_agent
from backend.models.schemas import DashboardSummary
from backend.security.audit_log import audit_chain
from backend.services.metrics_store import metrics_store

router = APIRouter()


class AuditQueryRequest(BaseModel):
    query: str = Field(min_length=1)


@router.get("/summary", response_model=DashboardSummary)
def summary() -> DashboardSummary:
    metrics = metrics_store.snapshot()
    return DashboardSummary(
        total_transactions=metrics.total_transactions,
        blocked_transactions=metrics.blocked_transactions,
        flagged_transactions=metrics.flagged_transactions,
        chain_size=len(audit_chain.all()),
    )


@router.get("/audit")
def audit() -> list[dict[str, str]]:
    return [entry.__dict__ for entry in audit_chain.all()]


@router.post("/audit/query")
def audit_query(request: AuditQueryRequest) -> dict[str, object]:
    matches = orchestrator_agent.audit_agent.query(request.query)
    return {"query": request.query, "count": len(matches), "matches": matches}


@router.get("/report")
def report() -> dict[str, str]:
    metrics = metrics_store.snapshot()
    summary_text = orchestrator_agent.report_agent.generate(
        total=metrics.total_transactions,
        flagged=metrics.flagged_transactions,
        blocked=metrics.blocked_transactions,
    )
    return {"report": summary_text}
