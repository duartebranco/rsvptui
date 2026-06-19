import json
import os

BOOKMARKS_DIR = os.path.expanduser("~/.config/rsvp-tui")
BOOKMARKS_FILE = os.path.join(BOOKMARKS_DIR, "bookmarks.json")


class BookmarkManager:

    @staticmethod
    def _ensure_dir():
        os.makedirs(BOOKMARKS_DIR, exist_ok=True)

    @staticmethod
    def _load_all() -> dict:
        if not os.path.exists(BOOKMARKS_FILE):
            return {}
        with open(BOOKMARKS_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def _save_all(bookmarks: dict):
        BookmarkManager._ensure_dir()
        with open(BOOKMARKS_FILE, "w") as f:
            json.dump(bookmarks, f, indent=2)

    @staticmethod
    def get(filepath: str) -> dict | None:
        bookmarks = BookmarkManager._load_all()
        return bookmarks.get(filepath)

    @staticmethod
    def set(filepath: str, index: int, wpm: int, mode: str):
        bookmarks = BookmarkManager._load_all()
        bookmarks[filepath] = {
            "filepath": filepath,
            "index": index,
            "wpm": wpm,
            "mode": mode,
        }
        BookmarkManager._save_all(bookmarks)

    @staticmethod
    def remove(filepath: str):
        bookmarks = BookmarkManager._load_all()
        bookmarks.pop(filepath, None)
        BookmarkManager._save_all(bookmarks)

    @staticmethod
    def maybe_resume(filepath: str, total_words: int) -> tuple:
        bookmark = BookmarkManager.get(filepath)
        if bookmark is None:
            return (0, 250, "auto")
        wpm = bookmark.get("wpm", 250)
        mode = bookmark.get("mode", "auto")
        answer = input(f"Resume at word {bookmark['index'] + 1}/{total_words}? (y/n) ")
        if answer.lower() != 'y':
            return (0, wpm, mode)
        return (bookmark["index"], wpm, mode)

    @staticmethod
    def save_or_remove(filepath: str, index: int, wpm: int, mode: str, finished: bool):
        if finished:
            BookmarkManager.remove(filepath)
        else:
            BookmarkManager.set(filepath, index, wpm, mode)
