# model.py
# book (text loading) class
# reader_state (current position, speed, pause)
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


class ReaderState:
    # holds current position, speed, pause

    def __init__(self, word_list: list[str], initial_wpm: int = 250):
        self.words = word_list
        self.total_words = len(word_list)
        self.current_index = 0          # 0‑based
        self.wpm = initial_wpm
        self.paused = False

    @property
    def current_word(self) -> str:
        if 0 <= self.current_index < self.total_words:
            return self.words[self.current_index]
        return ""

    @property
    def progress(self) -> float:
        if self.total_words == 0:
            return 0.0
        return self.current_index / self.total_words

    def next_word(self) -> bool:
        if self.current_index < self.total_words - 1:
            self.current_index += 1
            return True
        return False

    def previous_word(self) -> bool:
        if self.current_index > 0:
            self.current_index -= 1
            return True
        return False

    def is_finished(self) -> bool:
        return self.current_index >= self.total_words
