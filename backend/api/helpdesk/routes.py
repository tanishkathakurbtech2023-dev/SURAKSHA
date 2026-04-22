from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.agents.orchestrator import orchestrator_agent

router = APIRouter()


class HelpdeskRequest(BaseModel):
    message: str = Field(min_length=1)
    language: str = Field(default="en")


@router.post("/chat")
def chat(request: HelpdeskRequest) -> dict[str, str]:
    return orchestrator_agent.helpdesk_agent.respond(request.message, request.language)
