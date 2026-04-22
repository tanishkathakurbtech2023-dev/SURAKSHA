from dataclasses import dataclass

from backend.ml.risk_scoring.logistic_model import risk_model


@dataclass
class RiskScoreResult:
    score: float
    level: str
    challenge: str


def score_transaction(amount: float, device_trust: float, network_risk: float) -> RiskScoreResult:
    risk = round(risk_model.predict_proba(amount, device_trust, network_risk), 4)

    if risk < 0.35:
        return RiskScoreResult(score=risk, level="low", challenge="pin")
    if risk < 0.7:
        return RiskScoreResult(score=risk, level="medium", challenge="sms_otp")
    return RiskScoreResult(score=risk, level="high", challenge="biometric_plus_otp")
