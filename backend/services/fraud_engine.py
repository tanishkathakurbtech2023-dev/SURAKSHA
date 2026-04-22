from collections import defaultdict
from datetime import datetime, timedelta, timezone

from backend.ml.fraud_detection.lstm_model import lstm_model
from backend.ml.fraud_detection.random_forest_model import rf_validator


class FraudEngine:
    def __init__(self) -> None:
        self._history: dict[str, list[tuple[datetime, float]]] = defaultdict(list)

    def evaluate(self, user_id: str, amount: float, network_risk: float = 0.0) -> tuple[bool, str]:
        now = datetime.now(timezone.utc)
        recent_window = now - timedelta(minutes=10)
        transactions = [(t, a) for t, a in self._history[user_id] if t >= recent_window]
        amounts = [a for _, a in transactions]

        lstm_score = lstm_model.score(amounts, amount)
        rf_flag = rf_validator.predict_flag(amount=amount, velocity_count=len(transactions) + 1, network_risk=network_risk)

        transactions.append((now, amount))
        self._history[user_id] = transactions

        if lstm_score > 0.65 and rf_flag:
            return True, f"lstm_random_forest_consensus(score={lstm_score:.2f})"
        if amount >= 50000:
            return True, "high_single_transaction_amount"
        return False, "normal_pattern"


fraud_engine = FraudEngine()
