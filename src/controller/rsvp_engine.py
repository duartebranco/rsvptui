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

    def __init__(self, state: ReaderState, display: TerminalDisplay, stdscr):
        self.state = state
        self.display = display
        self.stdscr = stdscr
        self.running = True

    def run(self):
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
                mode=self.state.mode
            )

            # process input (non‑blocking)
            self._handle_input()

            if self.state.mode == ReaderState.MODE_AUTO:
                # if not paused and not finished, sleep for the required duration
                if not self.state.paused and not self.state.is_finished():
                    delay = 60.0 / self.state.wpm
                    # instead of sleeping the whole delay, we sleep in small chunks
                    # to keep the interface responsive to key presses.
                    self._responsive_sleep(delay)
                    # advance to next word
                    self.state.next_word()
                else:
                    # when paused, just sleep a short while to avoid CPU spinning
                    time.sleep(0.05)

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
        if key == ord('q'):
            self.running = False
        elif key == ord('?'):
            self.display.show_help()
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
        else:
            if key == ord('j') or key == ord('l'):
                self.state.next_word()
            elif key == ord('h') or key == ord('k'):
                self.state.previous_word()
            elif key == ord('+'):
                self.state.wpm = min(self.state.wpm + self.WPM_STEP, self.MAX_WPM)
            elif key == ord('-'):
                self.state.wpm = max(self.state.wpm - self.WPM_STEP, self.MIN_WPM)

    def _responsive_sleep(self, seconds: float):
        # sleep in short intervals so that pressing a key is detected quickly
        if seconds <= 0:
            return
        granularity = 0.02  # 20 ms
        slept = 0.0
        while slept < seconds and self.running and not self.state.paused:
            time.sleep(granularity)
            slept += granularity
            # check input during the sleep fragments
            self._handle_input()
