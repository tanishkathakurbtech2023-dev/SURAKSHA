class BERTLiteIntentClassifier:
    def predict_intent(self, text: str) -> str:
        t = text.lower()
        if any(w in t for w in ["otp", "pin", "code", "share"]):
            return "phishing_warning"
        if any(w in t for w in ["blocked", "failed", "declined"]):
            return "transaction_issue"
        return "general_help"


intent_classifier = BERTLiteIntentClassifier()
