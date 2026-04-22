class SentimentAnalyser:
    def analyse(self, text: str) -> str:
        t = text.lower()
        if any(w in t for w in ["urgent", "help", "scared", "fraud"]):
            return "distress"
        if any(w in t for w in ["thanks", "good", "ok"]):
            return "positive"
        return "neutral"


sentiment_analyser = SentimentAnalyser()
