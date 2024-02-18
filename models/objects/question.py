class Question:
    def __init__(self, text: str, vocal: str, hints: [str]):
        self.text: str = text
        self.vocal: str = vocal
        self.hints: [str] = hints

    def add_hint(self, text: str):
        self.hints.append(text)

    def remove_hint(self, text: str):
        self.hints.pop(text)
