class Question:
    def __init__(self, text_id: int, text: str, vocal: bytes, hints: [str]):
        self.test_id: int = text_id
        self.text: str = text
        self.vocal: bytes = vocal
        self.hints: [str] = hints

    def add_hint(self, text: str):
        self.hints.append(text)

    def remove_hint(self, text: str):
        self.hints.pop(text)
