from pydantic import BaseModel, Field


class RiskRequest(BaseModel):
    user_id: str = Field(min_length=1)
    amount: float = Field(ge=0)
    device_trust: float = Field(ge=0, le=1)
    network_risk: float = Field(ge=0, le=1)


class RiskResponse(BaseModel):
    score: float
    level: str
    challenge: str


class BehaviourRequest(BaseModel):
    session_features: list[float] = Field(default_factory=list)


class BehaviourResponse(BaseModel):
    isolation_score: float
    reconstruction_error: float
    trust_score: float
    reauth_required: bool


class TransactionRequest(BaseModel):
    user_id: str = Field(min_length=1)
    txn_id: str = Field(min_length=1)
    amount: float = Field(gt=0)
    to_account: str = Field(min_length=4)
    device_trust: float = Field(ge=0, le=1)
    network_risk: float = Field(ge=0, le=1)
    nonce: str = Field(min_length=8)


class TransactionResponse(BaseModel):
    txn_id: str
    risk_level: str
    auth_challenge: str
    fraud_flag: bool
    decision: str
    reason: str
    signature: str
    audit_hash: str
    recommended_action: str
    education_tip: str


class DashboardSummary(BaseModel):
    total_transactions: int
    blocked_transactions: int
    flagged_transactions: int
    chain_size: int
