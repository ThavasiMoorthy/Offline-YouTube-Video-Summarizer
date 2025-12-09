import os
from faster_whisper import WhisperModel

class Transcriber:
    def __init__(self, model_path="models/whisper", model_name="tiny.en", device="cpu", compute_type="int8"):
        """
        Initialize the Transcriber.
        Args:
            model_path: Path to the directory where models are stored/cached.
            model_name: Name of the Whisper model to load (e.g., "small.en").
        """
        # Ensure absolute path for model dir
        if not os.path.isabs(model_path):
            model_path = os.path.join(os.getcwd(), model_path)
            
        print(f"Loading Whisper model '{model_name}' from cache at {model_path}...")
        try:
            # We use model_name + download_root to load from the local cache structure
            # local_files_only=True ensures we don't try to hit the internet
            self.model = WhisperModel(model_name, device=device, compute_type=compute_type, download_root=model_path, local_files_only=True)
        except Exception as e:
            print(f"Failed to load local model. Error: {e}")
            raise e

    def transcribe(self, audio_path):
        """
        Transcribe the audio file and return the text.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print("Starting transcription...")
        segments, info = self.model.transcribe(audio_path, beam_size=5)
        
        print(f"Detected language '{info.language}' with probability {info.language_probability}")
        
        full_text = []
        for segment in segments:
            full_text.append(segment.text)
            
        return " ".join(full_text)
