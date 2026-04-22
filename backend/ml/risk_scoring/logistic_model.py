import math
from dataclasses import dataclass


@dataclass
class LogisticRiskModel:
    weights: tuple[float, float, float] = (2.2, 1.8, 1.2)
    bias: float = -1.6

    def predict_proba(self, amount: float, device_trust: float, network_risk: float) -> float:
        normalized_amount = min(max(amount / 10000, 0), 1)
        z = (
            self.bias
            + self.weights[0] * normalized_amount
            + self.weights[1] * (1 - device_trust)
            + self.weights[2] * network_risk
        )
        return 1 / (1 + math.exp(-z))


risk_model = LogisticRiskModel()
