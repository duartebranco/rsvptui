# view.py
# terminal display
import curses
import time


class TerminalDisplay:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)  # hide cursor
        self.height, self.width = stdscr.getmaxyx()

    def resize(self):
        self.height, self.width = self.stdscr.getmaxyx()

    def clear(self):
        self.stdscr.clear()

    def refresh(self):
        self.stdscr.refresh()

    def display_word(self, word: str, progress: float, wpm: int, paused: bool):
        # clear screen and draw word, progress bar, status line
        self.clear()

        # 1. centered word
        word_x = max(0, (self.width - len(word)) // 2)
        word_y = self.height // 2
        try:
            self.stdscr.addstr(word_y, word_x, word)
        except curses.error:
            # if word too long to fit:
            # truncate or just ignore (terminal will wrap)
            pass

        # 2. progress bar (20 characters wide)
        bar_width = min(40, self.width - 4)
        filled = int(progress * bar_width)
        bar = "[" + "#" * filled + "-" * (bar_width - filled) + "]"
        percent = int(progress * 100)
        progress_text = f" {percent}% {bar}"
        try:
            self.stdscr.addstr(self.height - 3, 0, progress_text[:self.width - 1])
        except curses.error:
            pass

        # 3. status line: WPM, pause indicator, help
        status = f" WPM: {wpm}   {'[PAUSED]' if paused else '[PLAYING]'}   +/- : adjust WPM   Space : pause/resume   q : quit"
        if len(status) > self.width:
            status = status[:self.width - 1]
        try:
            self.stdscr.addstr(self.height - 2, 0, status)
        except curses.error:
            pass

        self.refresh()

    def show_completion(self):
        # display end-of-book message
        self.clear()
        msg = "=== FINISHED! Press any key to exit ==="
        x = max(0, (self.width - len(msg)) // 2)
        y = self.height // 2
        try:
            self.stdscr.addstr(y, x, msg)
        except curses.error:
            pass
        self.refresh()
