class FraudReasoningAgent:
    def verdict(self, risk_level: str, fraud_flag: bool, fraud_reason: str) -> dict[str, str]:
        if fraud_flag and risk_level in {"medium", "high"}:
            return {
                "verdict": "block",
                "reasoning": f"Combined risk and fraud signal: {fraud_reason}",
                "recommended_action": "Block transaction and alert user immediately.",
            }
        if fraud_flag or risk_level == "high":
            return {
                "verdict": "flag",
                "reasoning": f"Suspicious pattern observed: {fraud_reason}",
                "recommended_action": "Hold for secondary verification.",
            }
        return {
            "verdict": "allow",
            "reasoning": "No significant anomaly detected.",
            "recommended_action": "Proceed normally.",
        }
