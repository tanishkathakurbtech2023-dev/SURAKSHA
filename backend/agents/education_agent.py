class EducationAgent:
    def tip(self, risk_level: str) -> str:
        if risk_level == "high":
            return "High risk detected: verify account details twice and avoid public Wi-Fi for transactions."
        if risk_level == "medium":
            return "Enable SMS alerts and confirm beneficiary details before transfer."
        return "Keep your PIN private and update app regularly for security patches."
