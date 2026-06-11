# main event loop and input handling
import curses
import time
from model.reader_state import ReaderState
from view.terminal_display import TerminalDisplay

class RSVPEngine:
    # orchestrates the reading session
    MIN_WPM = 60
    MAX_WPM = 800
    WPM_STEP = 10

    def __init__(self, state: ReaderState, display: TerminalDisplay, help_view, stdscr):
        self.state = state
        self.display = display
        self.help_view = help_view
        self.stdscr = stdscr
        self.running = True

    def run(self):
        # raw mode so Ctrl+C arrives as key code 3 instead of SIGINT
        curses.raw()
        # make getch() non‑blocking
        self.stdscr.nodelay(True)

        while self.running and not self.state.is_finished():
            # handle terminal resize
            self.display.resize()

            # display current word (or pause overlay)
            self.display.display_word(
                word=self.state.current_word,
                progress=self.state.progress,
                wpm=self.state.wpm,
                paused=self.state.paused,
                mode=self.state.mode,
                eta=self._compute_eta()
            )

            # process input (non‑blocking)
            self._handle_input()

            if self.state.mode == ReaderState.MODE_AUTO:
                # if not paused and not finished, sleep for the required duration
                if not self.state.paused and not self.state.is_finished():
                    delay = 60.0 / self.state.wpm

                    # sleep more if punctuation
                    if self.state.current_word.endswith(('.', '?', '!', ':', ';')):
                        delay *= 1.5

                    # instead of sleeping the whole delay, we sleep in small chunks
                    # to keep the interface responsive to key presses.
                    self._responsive_sleep(delay)

                    # advance to next word
                    self.state.next_word()
                else:
                    # when paused, just sleep a short while to avoid CPU spinning
                    time.sleep(0.05)
            else:  # MANUAL mode
                # avoid flickering: only sleep a short time
                time.sleep(0.02)

        # end of book
        self.display.show_completion()
        self.stdscr.nodelay(False)
        self.stdscr.getch()  # wait for any key to exit

    def _handle_input(self):
        try:
            key = self.stdscr.getch()
        except Exception:
            return

        # global keys
        if key == ord('q') or key == 3:  # Ctrl+C and q
            self.running = False
        elif key == ord('?'):
            self._show_help()
            return
        elif key == ord('m'):
            self.state.toggle_mode()
        elif key == ord('p') or key == ord(' '):
            if self.state.mode == ReaderState.MODE_AUTO:
                self.state.paused = not self.state.paused

        # mode‑specific keys
        if self.state.mode == ReaderState.MODE_AUTO:
            if key == ord('+') or key == ord('k'):
                self.state.wpm = min(self.state.wpm + self.WPM_STEP, self.MAX_WPM)
            elif key == ord('-') or key == ord('j'):
                self.state.wpm = max(self.state.wpm - self.WPM_STEP, self.MIN_WPM)
        else:  # MANUAL mode
            if key == ord('j'):
                self.state.next_word()
            elif key == ord('k'):
                self.state.previous_word()
            # allow +/- to still adjust WPM even in manual mode
            if key == ord('+'):
                self.state.wpm = min(self.state.wpm + self.WPM_STEP, self.MAX_WPM)
            elif key == ord('-'):
                self.state.wpm = max(self.state.wpm - self.WPM_STEP, self.MIN_WPM)

    def _show_help(self):
        self.stdscr.nodelay(False)
        scroll = 0
        while True:
            self.help_view.render(scroll)
            key = self.stdscr.getch()
            if key == ord('q') or key == 27:
                break
            elif key == ord('j') or key == curses.KEY_DOWN:
                max_y, _ = self.stdscr.getmaxyx()
                scroll = min(scroll + 1, max(0, len(self.help_view.lines) - (max_y - 2)))
            elif key == ord('k') or key == curses.KEY_UP:
                scroll = max(scroll - 1, 0)
        self.stdscr.clear()
        self.stdscr.refresh()
        self.stdscr.nodelay(True)

    def _compute_eta(self) -> str:
        remaining = max(0, len(self.state.words) - self.state.current_index)
        minutes = remaining / self.state.wpm
        if minutes >= 60:
            h = int(minutes) // 60
            m = int(minutes) % 60
            return f"ETA: {h}h{m:02d}m"
        elif minutes >= 1:
            return f"ETA: {int(minutes)} min"
        else:
            return "ETA: <1 min"

    def _responsive_sleep(self, seconds: float):
        # sleep in short intervals so that pressing a key is detected quickly
        if seconds <= 0:
            return
        granularity = 0.02
        slept = 0.0
        while slept < seconds and self.running and not self.state.paused:
            time.sleep(granularity)
            slept += granularity
            # check input during the sleep fragments
            self._handle_input()
