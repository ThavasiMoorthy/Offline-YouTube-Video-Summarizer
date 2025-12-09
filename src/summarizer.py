import requests
import json

class Summarizer:
    def __init__(self, model_name="llama3.1", api_url="http://localhost:11434/api/generate"):
        """
        Initialize the Summarizer using local Ollama instance.
        """
        self.model_name = model_name
        self.api_url = api_url
        print(f"Initialized Ollama Summarizer with model: {self.model_name}")

        # Add a check to ping the Ollama server
        # Extract the base URL from the api_url
        base_ollama_url = self.api_url.rsplit('/', 2)[0] # e.g., "http://localhost:11434" from "http://localhost:11434/api/generate"
        try:
            print(f"Pinging Ollama server at {base_ollama_url}...")
            # A simple GET request to the base URL usually indicates if the server is up
            response = requests.get(base_ollama_url, timeout=5)
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            print("Ollama server is running.")
        except requests.exceptions.ConnectionError:
            print(f"Error: Could not connect to Ollama server at {base_ollama_url}. Is it running? (Run 'ollama serve' in a terminal)")
            raise # Re-raise the exception to indicate that initialization failed
        except requests.exceptions.Timeout:
            print(f"Error: Timeout connecting to Ollama server at {base_ollama_url}.")
            raise
        except Exception as e:
            print(f"An unexpected error occurred while pinging Ollama: {e}")
            raise
        
    def summarize(self, text, min_length=150, max_length=500):
        """
        Summarize text using Ollama.
        """
        print("Sending text to Ollama for summarization...")
        
        prompt = f"""
        You are a helpful assistant. Please strictly summarize the following text into a concise and clear summary. 
        Do not repeat yourself. Capture the main points.
        
        TEXT:
        {text}
        
        SUMMARY:
        """
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3, # Low temp for factual summary
                "num_ctx": 2048     # Reduced context to prevent OOM on standard RAM
            }
        }
        
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            summary = result.get("response", "")
            return summary.strip()
            
        except requests.exceptions.ConnectionError:
            return "Error: Could not connect to Ollama. Is it running? (Run 'ollama serve' in a terminal)"
        except Exception as e:
            print(f"Ollama Error: {e}")
            return f"Error generating summary: {e}"
