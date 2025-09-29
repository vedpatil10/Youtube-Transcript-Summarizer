# YouTube Transcript Summarizer

Concise summaries of YouTube video transcripts. Paste a YouTube URL and get a TL;DR generated with TextRank.

## Features
- Fetches public transcripts using `youtube-transcript-api`
- Summarizes with TextRank (via `sumy`)
- Simple Flask backend + clean UI
- Adjustable summary length

## Tech Stack
- Backend: Flask
- NLP: sumy (TextRank), youtube-transcript-api
- Frontend: HTML, CSS, JavaScript

## Setup
```bash
python -m venv .venv
.venv\\Scripts\\activate  # Windows PowerShell
pip install -r requirements.txt
python run.py
```
App will run at `http://localhost:5000`.

## Usage
1. Paste a full YouTube URL (e.g., `https://www.youtube.com/watch?v=VIDEO_ID`)
2. Adjust the summary length slider
3. Click Summarize

## Notes
- Works for videos with available transcripts (manual or auto-generated if allowed)
- Some videos disable transcripts; you'll get a friendly error

## Deploy (optional)
- Use `gunicorn` on Linux servers: `gunicorn -w 2 -b 0.0.0.0:8000 run:app`

## License
MIT


