# reader_state (current position, speed, pause)

class ReaderState:
    # holds current position, speed, pause

    MODE_AUTO = "auto"
    MODE_MANUAL = "manual"

    def __init__(self, word_list: list[str], initial_wpm: int = 250):
        self.words = word_list
        self.total_words = len(word_list)
        self.current_index = 0          # 0‑based
        self.wpm = initial_wpm
        self.paused = False
        self.mode = self.MODE_AUTO   # auto or manual

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

    def toggle_mode(self):
        self.mode = self.MODE_MANUAL if self.mode == self.MODE_AUTO else self.MODE_AUTO
        # when switching to manual mode, ensure we are not paused
        if self.mode == self.MODE_MANUAL:
            self.paused = False   # manual mode overrides auto timer
