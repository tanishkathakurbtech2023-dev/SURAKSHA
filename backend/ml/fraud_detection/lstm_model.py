from statistics import mean


class LSTMSequenceModel:
    """Lightweight sequence anomaly approximation for prototype runtime."""

    def score(self, recent_amounts: list[float], current_amount: float) -> float:
        if not recent_amounts:
            return 0.0
        baseline = max(mean(recent_amounts), 1.0)
        return min(abs(current_amount - baseline) / baseline, 1.0)


lstm_model = LSTMSequenceModel()
