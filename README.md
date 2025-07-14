# YouTube Video Downloader GUI

A simple Python desktop app with a graphical interface to download YouTube videos, select video and audio formats, and optionally merge them using `ffmpeg`.

---

## Features

- Paste a YouTube URL
- Fetch and display available video and audio formats separately
- Choose video and audio streams from dropdown menus
- Optionally merge video and audio for high-quality downloads
- Automatic merging with `ffmpeg` if enabled
- Saves downloaded videos in the current directory with the video title as filename

---

## Prerequisites

- Python 3.7+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://ffmpeg.org/) (required for merging video and audio)
- Tkinter (usually bundled with Python; if not, install via your OS package manager, e.g., `sudo apt install python3-tk`)

---

## Installation

1. Clone or download this repository.

2. Install Python dependencies:

   ```bash
    pip install yt-dlp
   ```

Install Python dependencies:
   ```bash
      pip install yt-dlp
   ```

Install ffmpeg:

On Debian/Ubuntu:

   ```bash
      sudo apt install ffmpeg
   ```
On macOS (with Homebrew):

    brew install ffmpeg

On Windows:
    Download and install from ffmpeg.org, and ensure ffmpeg is in your system PATH.


## Usage

Run the application:

   ```bash
      python yt_gui_downloader.py
   ```