import curses

class HelpView:
    # pure view: renders help content, no event loop
    def __init__(self, stdscr):
        self.stdscr = stdscr
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

    def render(self, scroll: int):
        self.stdscr.clear()
        max_y, max_x = self.stdscr.getmaxyx()
        try:
            self.stdscr.addstr(0, 2, "RSVP TUI - Help (press q to close)")
        except curses.error:
            pass
        for idx, line in enumerate(self.lines[scroll:scroll + max_y - 2]):
            try:
                self.stdscr.addstr(idx + 1, 2, line[:max_x - 4])
            except curses.error:
                pass
        self.stdscr.refresh()
