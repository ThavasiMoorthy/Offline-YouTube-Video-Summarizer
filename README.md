# Offline YouTube Video Summarizer

A robust, offline-first AI application that downloads, transcribes, and summarizes YouTube videos locally on your machine.

## Project Overview
This tool allows users to input a YouTube URL and receive a concise, accurate summary of the video's content. It is built with **privacy, speed, and offline capability** in mind.

It intelligently switches between:
1.  **Instant Mode**: Fetches existing subtitles (if available) for near-instant results.
2.  **AI Mode**: Uses local Speech-to-Text (Whisper) to listen and transcribe audio if no subtitles exist.

Final summarization is performed by **Llama 3.2 (1B)** via Ollama, ensuring high-quality, human-like summaries without sending data to third-party clouds.

## Features
- **Instant Captions**: Automatically bypasses transcription if YouTube subtitles exist (1s processing).
- **Offline Processing**: All AI models run locally. No internet required after initial setup.
- **Speech-to-Text**: `faster-whisper` (Tiny model) for fast CPU transcription when needed.
- **Smart Summarization**: Uses `Ollama` + `Llama 3.2 (1B)` to generate coherent, non-repetitive summaries.
- **Web Interface**: Clean, responsive UI with lazy-loading for instant startup.

## Setup and Installation

### Prerequisites
1.  **Python 3.8+**
2.  **[Ollama](https://ollama.com/)** installed and running.

### 1. Setup Ollama
Ensure Ollama is installed. Then, pull the required model (approx 1.3GB):
```bash
ollama pull llama3.2:1b
```

### 2. Clone and Setup Environment
```bash
git clone <your-repo-url>
cd offline_summarizer

# Create and activate virtual environment (Windows)
python -m venv venv
.\venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Download Whisper Model
Run the setup script to download the specific `faster-whisper` model (Tiny) to the `models/` directory:
```bash
python download_models.py
```

## Usage

### Run the App
1.  Make sure Ollama is running (`ollama serve`).
2.  Start the web server:
    ```bash
    python app.py
    ```
3.  Open your browser and navigate to `http://127.0.0.1:8000`.

### Summarize a Video
1.  Paste a YouTube URL.
2.  Click **Generate Summary**.
3.  **Result**:
    - If captions exist: Result appears in ~5-10 seconds.
    - If no captions: Audio is downloaded and transcribed (approx 10-20% of video duration).

## Design Choices & Justifications

### 1. Architecture: Single-Responsibility Principle
The application is split into `downloader.py` (Handling YouTube/FFmpeg), `transcriber.py` (Handling Whisper), and `summarizer.py` (Handling Ollama). This made refactoring easy when we switched from BART to Ollama.

### 2. Summarization Model: Llama 3.2 (1B) vs BART
- **Initial Approach**: We started with `distilbart-cnn`.
- **Problem**: BART models frequently suffered from "repetition loops" (repeating the same phrase infinitely) and had a hard token limit (1024 tokens).
- **Pivoting to Llama 3.2 (1B)**: 
    - **Quality**: significantly smarter and more coherent.
    - **Context**: Handles larger context natively (up to 128k, restricted to 2k for RAM efficiency).
    - **Size**: At 1.3GB, it is "heavy" but 3x lighter than standard 7B models, making it the perfect balance for consumer hardware.

### 3. "Instant Mode" (The Speed Optimization)
- **Challenge**: AI transcription (Whisper) is computationally expensive. Even the "Tiny" model takes time.
- **Optimization**: We implemented a check using `youtube-transcript-api`. 
- **Result**: For 95% of videos (which have captions), processing time dropped from **60s** to **2s**. This was a critical UX improvement.

## Challenges Faced

### 1. The "Syndrome Syndrome" Loop
**Issue**: The HuggingFace `pipeline` summarizer would get stuck repeating tokens ("syndrome syndrome syndrome...") indefinitely.
**Solution**: Initially tried beam search penalties (`no_repeat_ngram_size`). While this stopped loops, it made generation slow (4x slower).
**Final Fix**: Switched to **Llama 3.2**, which is architecturally superior and does not suffer from these basic degeneration issues.

### 2. Zombie Processes (Port 8000 in use)
**Issue**: Restarting the Python server often left "zombie" processes holding port 8000, causing the app to hang indefinitely on loading.
**Solution**: Learned to use `netstat -ano` to identify PIDs and `taskkill` to forcefully clean up the environment before restarts.

### 3. Startup Time
**Issue**: Loading AI models at startup made the server take 30s+ to become responsive.
**Solution**: Implemented **Lazy Loading**. The server starts instantly, and models are only loaded into memory when the first request is made.
