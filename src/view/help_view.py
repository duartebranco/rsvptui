import curses

class HelpView:
    # help panel

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.lines = [
            "=== RSVP TUI Help ===",
            "",
            "Modes:",
            "  Auto mode     - words advance automatically at WPM",
            "  Manual mode   - press j/k to move word by word",
            "",
            "Keys in AUTO mode:",
            "  + or k        - increase WPM",
            "  - or j        - decrease WPM",
            "  Space or p    - pause / resume",
            "",
            "Keys in MANUAL mode:",
            "  j             - next word",
            "  k             - previous word",
            "",
            "Global keys (any mode):",
            "  m             - toggle Auto/Manual mode",
            "  ?             - show this help",
            "  q             - quit program",
            "",
            "Navigation inside help:",
            "  j / Down      - scroll down",
            "  k / Up        - scroll up",
            "  q or ESC      - close help",
        ]
        self.scroll = 0

    def show(self):
        curses.curs_set(0)
        self.stdscr.clear()
        while True:
            self._draw()
            key = self.stdscr.getch()
            if key == ord('q') or key == 27:  # q or ESC
                break
            elif key == ord('j') or key == curses.KEY_DOWN:
                self.scroll = min(self.scroll + 1, max(0, len(self.lines) - (self.height - 2)))
            elif key == ord('k') or key == curses.KEY_UP:
                self.scroll = max(self.scroll - 1, 0)
        # clean up and redraw later by caller
        self.stdscr.clear()
        self.stdscr.refresh()
        curses.curs_set(0)  # restore cursor hidden

    def _draw(self):
        self.stdscr.clear()
        max_y, max_x = self.stdscr.getmaxyx()
        # title
        try:
            self.stdscr.addstr(0, 2, "RSVP TUI - Help (press q to close)")
        except curses.error:
            pass
        # draw visible lines
        for idx, line in enumerate(self.lines[self.scroll:self.scroll + max_y - 2]):
            try:
                self.stdscr.addstr(idx + 1, 2, line[:max_x - 4])
            except curses.error:
                pass
        self.stdscr.refresh()
