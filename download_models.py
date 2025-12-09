import os
import shutil
from faster_whisper import WhisperModel
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Define paths for offline storage
MODEL_DIR = os.path.join(os.getcwd(), "models")
WHISPER_DIR = os.path.join(MODEL_DIR, "whisper")
SUMMARIZER_DIR = os.path.join(MODEL_DIR, "summarizer")

def download_models():
    print(f"Creating model directory at {MODEL_DIR}...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # 1. Download Faster-Whisper Model
    # We use 'tiny.en' for maximum speed on CPU (Switch back to 'small.en' or 'medium.en' for accuracy)
    print("Downloading Faster-Whisper model (tiny.en)...")
    # This downloads to the cache dir by default, but we want to be explicit for "offline" portability
    model = WhisperModel("tiny.en", device="cpu", compute_type="int8", download_root=WHISPER_DIR)
    print(f"Faster-Whisper model saved to {WHISPER_DIR}")

    # 2. Download Summarization Model (DistilBART)
    print("Downloading Summarization model (sshleifer/distilbart-cnn-12-6)...")
    model_name = "sshleifer/distilbart-cnn-12-6"
    
    # Download and save tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    tokenizer.save_pretrained(SUMMARIZER_DIR)
    model.save_pretrained(SUMMARIZER_DIR)
    print(f"Summarization model saved to {SUMMARIZER_DIR}")
    
    print("All models downloaded successfully!")

if __name__ == "__main__":
    download_models()
