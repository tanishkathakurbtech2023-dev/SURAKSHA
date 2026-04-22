from backend.agents.audit_agent import AuditQueryAgent
from backend.agents.education_agent import EducationAgent
from backend.agents.fraud_agent import FraudReasoningAgent
from backend.agents.helpdesk_agent import NLPHelpdeskAgent
from backend.agents.report_agent import ReportDigestAgent


class RiskOrchestratorAgent:
    def __init__(self) -> None:
        self.fraud_agent = FraudReasoningAgent()
        self.helpdesk_agent = NLPHelpdeskAgent()
        self.report_agent = ReportDigestAgent()
        self.education_agent = EducationAgent()
        self.audit_agent = AuditQueryAgent()


orchestrator_agent = RiskOrchestratorAgent()
