from fastapi import APIRouter

from backend.ml.biometrics.autoencoder_model import autoencoder_profiler
from backend.ml.biometrics.isolation_forest_model import isolation_forest_profiler
from backend.ml.risk_scoring.scorer import score_transaction
from backend.models.schemas import BehaviourRequest, BehaviourResponse, RiskRequest, RiskResponse

router = APIRouter()


@router.post("/risk", response_model=RiskResponse)
def compute_risk(request: RiskRequest) -> RiskResponse:
    result = score_transaction(
        amount=request.amount,
        device_trust=request.device_trust,
        network_risk=request.network_risk,
    )
    return RiskResponse(score=result.score, level=result.level, challenge=result.challenge)


@router.post("/behaviour", response_model=BehaviourResponse)
def behaviour_profile(request: BehaviourRequest) -> BehaviourResponse:
    isolation_score = round(isolation_forest_profiler.anomaly_score(request.session_features), 4)
    reconstruction_error = round(autoencoder_profiler.reconstruction_error(request.session_features), 4)
    trust_score = round(max(0.0, 1 - ((isolation_score + reconstruction_error) / 2)), 4)
    reauth_required = trust_score < 0.5

    return BehaviourResponse(
        isolation_score=isolation_score,
        reconstruction_error=reconstruction_error,
        trust_score=trust_score,
        reauth_required=reauth_required,
    )
