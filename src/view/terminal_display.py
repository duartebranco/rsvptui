# terminal display
import curses

class TerminalDisplay:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)  # hide cursor
        self.height, self.width = stdscr.getmaxyx()
        self._init_colors()

    def _init_colors(self):
        # set color pair for ORP highlighting
        if curses.has_colors():
            curses.start_color()
            try:
                curses.use_default_colors()
                curses.init_pair(1, curses.COLOR_YELLOW, -1)
            except curses.error:
                curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def resize(self):
        self.height, self.width = self.stdscr.getmaxyx()

    def clear(self):
        self.stdscr.clear()

    def refresh(self):
        self.stdscr.refresh()

    def _get_orp_index(self, word: str) -> int:
        # returns index of optimal recognition point (ORP)
        if not word:
            return 0
        return (len(word) - 1) // 2

    def _display_colored_word(self, y: int, x: int, word: str):
        # draw word with ORP highlighted
        if not word:
            return
        orp_idx = self._get_orp_index(word)
        # draw left part (before ORP)
        if orp_idx > 0:
            try:
                self.stdscr.addstr(y, x, word[:orp_idx])
            except curses.error:
                pass
        # draw ORP letter with colour
        try:
            if curses.has_colors():
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x + orp_idx, word[orp_idx])
                self.stdscr.attroff(curses.color_pair(1))
            else:
                # fallback
                self.stdscr.attron(curses.A_REVERSE)
                self.stdscr.addstr(y, x + orp_idx, word[orp_idx])
                self.stdscr.attroff(curses.A_REVERSE)
        except curses.error:
            pass
        # draw right part (after ORP)
        if orp_idx + 1 < len(word):
            try:
                self.stdscr.addstr(y, x + orp_idx + 1, word[orp_idx + 1:])
            except curses.error:
                pass

    def display_word(self, word: str, progress: float, wpm: int, paused: bool, mode: str):
        # clear screen and draw word, progress bar, status line
        self.clear()

        # centered word
        word_x = max(0, (self.width - len(word)) // 2)
        word_y = self.height // 2
        self._display_colored_word(word_y, word_x, word)

        # progress bar
        bar_width = min(40, self.width - 4)
        filled = int(progress * bar_width)
        bar = "[" + "#" * filled + "-" * (bar_width - filled) + "]"
        percent = int(progress * 100)
        progress_text = f" {percent}% {bar}"
        try:
            self.stdscr.addstr(self.height - 4, 0, progress_text[:self.width - 1])
        except curses.error:
            pass

        # status line: WPM, pause indicator, help, mode
        mode_indicator = "MANUAL" if mode == "manual" else "AUTO"
        if mode == "auto":
            speed_hint = "j/k : speed"
        else:
            speed_hint = "j : next word   k : prev word"
        status = f" [{mode_indicator}]  WPM: {wpm}  {'[PAUSED]' if paused else '[PLAYING]'}  |  {speed_hint}"
        if len(status) > self.width:
            status = status[:self.width - 1]
        try:
            self.stdscr.addstr(self.height - 3, 0, status)
        except curses.error:
            pass

        # bottom hint line
        hint = " Space/p: pause  m: toggle mode  ?: help  q: quit"
        if len(hint) > self.width:
            hint = hint[:self.width - 1]
        try:
            self.stdscr.addstr(self.height - 2, 0, hint)
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
