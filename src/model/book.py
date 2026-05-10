# book (text loading) class
import os

class Book:
    # load a text file and tokenise into words (keeps punctuation attached)

    def __init__(self, filepath: str):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"{filepath} not found")
        with open(filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()
        self.words = self._tokenise(raw_text)

    # split whitespace
    @staticmethod
    def _tokenise(text: str) -> list[str]:
        return [word for word in text.split() if word]
