import argparse
import curses
import sys
from model import Book, ReaderState
from view import TerminalDisplay
from controller import RSVPEngine


def main(stdscr):
    # parse command line argument
    parser = argparse.ArgumentParser(description="RSVP terminal ebook reader")
    parser.add_argument("file", help="Path to text file")
    args = parser.parse_args()

    # load book
    try:
        book = Book(args.file)
    except Exception as e:
        raise RuntimeError(f"Failed to load file: {e}")

    # create model, view, controller
    state = ReaderState(book.words, initial_wpm=250)
    display = TerminalDisplay(stdscr)
    engine = RSVPEngine(state, display, stdscr)

    # run the reader
    engine.run()


if __name__ == "__main__":
    curses.wrapper(main)
