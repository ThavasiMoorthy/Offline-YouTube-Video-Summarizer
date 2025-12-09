# Offline YouTube Video Summarizer - Walkthrough

## Overview
This application downloads, transcribes, and summarizes YouTube videos entirely offline, ensuring privacy and zero dependency on cloud APIs.

## Features Completed
- [x] **Audio Downloader**: Fetches audio from YouTube (supports raw formats like m4a/webm).
- [x] **Offline STT**: Uses `faster-whisper` (Tiny model) for fast CPU transcription.
- [x] **Instant Captions**: Automatically fetches YouTube subtitles if available (1s processing).
- [x] **Offline Summarizer**: Uses `Ollama` + `Llama 3.2 (1B)` for high-quality, fast generation.
- [x] **Web Interface**: Clean, responsive UI with lazy-loading for instant startup.
- [x] **Cross-Platform**: Tested on Windows (with `venv`).

## How to Run
1. **Ensure Ollama is Running**:
   ```powershell
   ollama serve
   ```
2. **Activate Virtual Environment**:
   ```powershell
   .\venv\Scripts\activate
   ```
3. **Start Server**:
   ```powershell
   python app.py
   ```
4. **Open Browser**:
   Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Performance Notes
- **Instant Mode**: If a video has subtitles, the summary is generated in ~5-10 seconds.
- **Fallback Mode**: If no subtitles, AI transcription runs (~10-20% of video duration).
- **English Videos**: Fastest processing.
- **Hardware**: Processing speed depends heavily on your CPU.

## Troubleshooting
- **"500 Internal Server Error"**: Ensure `ollama` is running and `llama3.2:1b` is pulled (`ollama pull llama3.2:1b`).
- **"Port 8000 in use"**: Kill stray python processes via `taskkill /F /IM python.exe`.
