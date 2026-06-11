# reader_state (current position, speed, pause)

class ReaderState:
    # holds current position, speed, pause

    MODE_AUTO = "auto"
    MODE_MANUAL = "manual"

    def __init__(self, word_list: list[str], initial_wpm: int = 250,
                 initial_index: int = 0, initial_mode: str = "auto",
                 paragraph_ranges: list | None = None,
                 chapter_starts: list | None = None):
        self.words = word_list
        self.total_words = len(word_list)
        self.current_index = initial_index
        self.wpm = initial_wpm
        self.paused = False
        self.mode = initial_mode
        self.paragraph_ranges = paragraph_ranges or [(0, len(word_list))]
        self.chapter_starts = chapter_starts or []

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
        # manual mode overrides auto timer
        if self.mode == self.MODE_MANUAL:
            self.paused = False

    def find_paragraph(self, word_idx: int | None = None) -> int:
        idx = word_idx if word_idx is not None else self.current_index
        for i, (start, end) in enumerate(self.paragraph_ranges):
            if start <= idx < end:
                return i
        return max(0, len(self.paragraph_ranges) - 1)

    def find_chapter(self, word_idx: int | None = None) -> int:
        idx = word_idx if word_idx is not None else self.current_index
        for i, (start, _) in enumerate(self.chapter_starts):
            next_start = self.chapter_starts[i + 1][0] if i + 1 < len(self.chapter_starts) else float('inf')
            if start <= idx < next_start:
                return i
        return max(0, len(self.chapter_starts) - 1)

    def get_paragraph_text(self, para_idx: int) -> str:
        if 0 <= para_idx < len(self.paragraph_ranges):
            start, end = self.paragraph_ranges[para_idx]
            return ' '.join(self.words[start:end])
        return ""

    def get_chapter_title(self, ch_idx: int) -> str:
        if 0 <= ch_idx < len(self.chapter_starts):
            return self.chapter_starts[ch_idx][1]
        return ""

    def find_first_para_of_chapter(self, ch_idx: int) -> int:
        if not self.chapter_starts or ch_idx >= len(self.chapter_starts):
            return 0
        ch_start = self.chapter_starts[ch_idx][0]
        for i, (start, _) in enumerate(self.paragraph_ranges):
            if start >= ch_start:
                return i
        return 0
