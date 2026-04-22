class RandomForestValidator:
    """Rule-ensemble stand-in for random forest confidence."""

    def predict_flag(self, amount: float, velocity_count: int, network_risk: float) -> bool:
        votes = 0
        votes += 1 if amount > 25000 else 0
        votes += 1 if velocity_count >= 4 else 0
        votes += 1 if network_risk > 0.7 else 0
        return votes >= 2


rf_validator = RandomForestValidator()
