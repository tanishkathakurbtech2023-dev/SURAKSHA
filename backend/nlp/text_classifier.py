class IncidentTextClassifier:
    def classify(self, text: str) -> str:
        t = text.lower()
        if "otp" in t or "phishing" in t:
            return "phishing"
        if "upi" in t or "transaction" in t:
            return "transaction_fraud"
        return "general_security"


text_classifier = IncidentTextClassifier()
