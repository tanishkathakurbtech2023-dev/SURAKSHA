from fastapi import APIRouter

from backend.services.fraud_engine import fraud_engine

router = APIRouter()


@router.get("/ping")
def ping_fraud_engine() -> dict[str, str]:
    return {"fraud_engine": "ready"}


@router.get("/simulate")
def simulate(user_id: str, amount: float) -> dict[str, str | bool]:
    flag, reason = fraud_engine.evaluate(user_id=user_id, amount=amount)
    return {"flag": flag, "reason": reason}
