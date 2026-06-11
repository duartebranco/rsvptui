# book (text loading) class
import os
import re

class Book:
    # load a text file and tokenise into words (keeps punctuation attached)

    def __init__(self, filepath: str):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"{filepath} not found")
        with open(filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()
        self.words, self.paragraph_ranges, self.chapter_starts = self._parse_text(raw_text)

    @staticmethod
    def _parse_text(text: str):
        # split text into words, paragraph ranges and chapter starts.
        blocks = re.split(r'\n[ \t]*\n', text)

        words: list[str] = []
        paragraph_ranges: list[tuple[int, int]] = []
        chapter_starts: list[tuple[int, str]] = []

        word_offset = 0

        for block in blocks:
            block = block.strip()
            if not block:
                continue

            block_words = block.split()
            words.extend(block_words)
            para_end = word_offset + len(block_words)
            paragraph_ranges.append((word_offset, para_end))

            heading_match = re.match(r'^#{1,6}\s+(.+)$', block, re.MULTILINE)
            if heading_match:
                title = heading_match.group(1).strip()
                chapter_starts.append((word_offset, title))

            word_offset = para_end

        return words, paragraph_ranges, chapter_starts
