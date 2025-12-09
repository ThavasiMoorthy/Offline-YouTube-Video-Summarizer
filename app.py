import os
import shutil
from fastapi import FastAPI, BackgroundTasks, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

from src.downloader import AudioDownloader
from src.transcriber import Transcriber
from src.summarizer import Summarizer

app = FastAPI(title="Offline YouTube Summarizer")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize Downloader (Fast)
os.makedirs("downloads", exist_ok=True)
downloader = AudioDownloader("downloads")

# Global placeholders for Heavy Models
transcriber = None
summarizer = None

def get_models():
    """Lazily load models if they aren't loaded yet."""
    global transcriber, summarizer
    if transcriber is None or summarizer is None:
        print("Lazy-loading models...")
        try:
            # Check model paths
            if os.path.exists("models/whisper") and os.path.exists("models/summarizer"):
                if transcriber is None:
                     transcriber = Transcriber("models/whisper", model_name="tiny.en")
                if summarizer is None:
                     # Use Llama 3.2 (1B) for speed
                     summarizer = Summarizer(model_name="llama3.2:1b")
            else:
                print("WARNING: Models not found in 'models/' directory.")
        except Exception as e:
            print(f"Error loading models: {e}")
            raise e
    return transcriber, summarizer

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/summarize", response_class=HTMLResponse)
async def handle_summarize(request: Request, url: str = Form(...)):
    global transcriber, summarizer
    
    # Ensure models are loaded
    try:
        get_models()
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": f"Failed to load models: {str(e)}"
        })

    if not transcriber or not summarizer:
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": "Models not loaded. Server setup incomplete."
        })
    
    try:
        # 1. Try Instant Transcript (Captions)
        print(f"Checking for captions for {url}...")
        transcript = downloader.get_transcript(url)
        
        if transcript:
            print("Captions found! Skipping audio download & transcription.")
            title = "YouTube Video (Instant Captions)" 
        else:
            # 2. Fallback: Download & Transcribe
            print(f"No captions found. Downloading audio {url}...")
            audio_path, title = downloader.download_audio(url)
            
            # 3. Transcribe
            print(f"Transcribing {title}...")
            transcript = transcriber.transcribe(audio_path)
            
            # Cleanup audio file
            try:
               if os.path.exists(audio_path):
                   os.remove(audio_path)
            except:
                pass
        
        # 4. Summarize (Common step)
        print(f"Summarizing (Length: {len(transcript)} chars)...")
        summary_text = summarizer.summarize(transcript)
            
        return templates.TemplateResponse("result.html", {
            "request": request,
            "title": title,
            "summary": summary_text,
            "transcript": transcript[:500] + "..." 
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": f"Error processing video: {str(e)}"
        })

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
