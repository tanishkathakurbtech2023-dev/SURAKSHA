import re


class NERModel:
    def extract_entities(self, text: str) -> dict[str, list[str]]:
        accounts = re.findall(r"\b[A-Z]{3,}[0-9]{3,}\b", text)
        money = re.findall(r"\b\d+(?:\.\d+)?\b", text)
        return {"accounts": accounts, "amounts": money}


ner_model = NERModel()
