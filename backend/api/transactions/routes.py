from fastapi import APIRouter, HTTPException

from backend.agents.orchestrator import orchestrator_agent
from backend.ml.risk_scoring.scorer import score_transaction
from backend.models.schemas import TransactionRequest, TransactionResponse
from backend.security.audit_log import audit_chain
from backend.security.encryption import encrypt_payload
from backend.security.signatures import sign_transaction
from backend.services.fraud_engine import fraud_engine
from backend.services.metrics_store import metrics_store
from backend.services.nonce_store import nonce_store

router = APIRouter()


@router.post("/process", response_model=TransactionResponse)
def process_transaction(request: TransactionRequest) -> TransactionResponse:
    if not nonce_store.use_nonce(request.nonce):
        raise HTTPException(status_code=409, detail="duplicate_nonce_detected")

    risk = score_transaction(
        amount=request.amount,
        device_trust=request.device_trust,
        network_risk=request.network_risk,
    )
    fraud_flag, fraud_reason = fraud_engine.evaluate(request.user_id, request.amount, request.network_risk)

    agent_verdict = orchestrator_agent.fraud_agent.verdict(
        risk_level=risk.level,
        fraud_flag=fraud_flag,
        fraud_reason=fraud_reason,
    )
    decision = agent_verdict["verdict"]

    encrypted = encrypt_payload(
        f"{request.user_id}:{request.txn_id}:{request.amount}:{request.to_account}:{request.nonce}"
    )
    signature = sign_transaction(encrypted)
    education_tip = orchestrator_agent.education_agent.tip(risk.level)

    audit_entry = audit_chain.append(
        event="transaction_processed",
        payload=(
            f"txn_id={request.txn_id};decision={decision};risk={risk.level};fraud={fraud_flag};"
            f"agent_reason={agent_verdict['reasoning']}"
        ),
    )

    metrics_store.record(flagged=(decision == "flag"), blocked=(decision == "block"))

    return TransactionResponse(
        txn_id=request.txn_id,
        risk_level=risk.level,
        auth_challenge=risk.challenge,
        fraud_flag=fraud_flag,
        decision=decision,
        reason=agent_verdict["reasoning"],
        signature=signature,
        audit_hash=audit_entry.hash,
        recommended_action=agent_verdict["recommended_action"],
        education_tip=education_tip,
    )
