# rsvptui

Minimal Rapid Serial Visual Presentation (RSVP) reader for plain text files.

## Features

- Flash words one by one in the centre of the terminal.
- Adjust words per minute (WPM) with `+` / `-` (range 60–800).
- Pause / resume with `Space`.
- Real‑time progress bar, WPM and ETA display.
- Two modes: Auto (continuous) and Manual (step through with `j`/`k`).
- Chapter navigation with `[` / `]` (shows heading + content overview).
- Paragraph navigation with `Ctrl+j` / `Ctrl+k` (shows content overview).
- Punctuation pause — extra delay after sentences.
- Resume prompt on startup (bookmarks stored at `~/.config/rsvp-tui/bookmarks.json`).
- Quit with `q`.

## Requirements

- Python 3.10+
- No external packages – uses only the standard library.

## Usage

```bash
python main.py samples/chapter-test.txt
```
