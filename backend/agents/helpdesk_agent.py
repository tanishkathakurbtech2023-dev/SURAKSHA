from backend.nlp.intent_classifier import intent_classifier
from backend.nlp.ner_model import ner_model
from backend.nlp.sentiment_analyser import sentiment_analyser
from backend.nlp.text_classifier import text_classifier


class NLPHelpdeskAgent:
    def respond(self, message: str, language: str = "en") -> dict[str, object]:
        intent = intent_classifier.predict_intent(message)
        sentiment = sentiment_analyser.analyse(message)
        entities = ner_model.extract_entities(message)
        category = text_classifier.classify(message)

        if intent == "phishing_warning":
            reply = "Never share OTP/PIN with anyone. Bank staff will never ask for it."
        elif intent == "transaction_issue":
            reply = "Your transaction may be blocked for safety. Verify beneficiary and retry securely."
        else:
            reply = "Stay safe: verify links, check beneficiary name, and report suspicious calls immediately."

        return {
            "language": language,
            "intent": intent,
            "sentiment": sentiment,
            "incident_category": category,
            "entities": entities,
            "reply": reply,
        }
