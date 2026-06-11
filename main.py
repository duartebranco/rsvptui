import argparse
import curses
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from src.model.book import Book
from src.model.reader_state import ReaderState
from src.view.terminal_display import TerminalDisplay
from src.view.help_view import HelpView
from src.controller.rsvp_engine import RSVPEngine
from src.utils.bookmarks import BookmarkManager

def main():
    parser = argparse.ArgumentParser(description="RSVP terminal ebook reader")
    parser.add_argument("file", help="Path to text file")
    args = parser.parse_args()

    # load book
    try:
        book = Book(args.file)
    except Exception as e:
        raise RuntimeError(f"Failed to load file: {e}") from e

    filepath = os.path.abspath(args.file)

    # ask to resume from bookmark
    initial_index, initial_wpm, initial_mode = BookmarkManager.maybe_resume(
        filepath, len(book.words),
    )

    # run the reader
    def _run(stdscr):
        state = ReaderState(
            book.words,
            initial_wpm=initial_wpm,
            initial_index=initial_index,
            initial_mode=initial_mode,
        )
        display = TerminalDisplay(stdscr)
        help_view = HelpView(stdscr)
        engine = RSVPEngine(state, display, help_view, stdscr)
        engine.run()

        BookmarkManager.save_or_remove(
            filepath, state.current_index, state.wpm, state.mode,
            finished=state.is_finished(),
        )

    curses.wrapper(_run)


if __name__ == "__main__":
    main()
