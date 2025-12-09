from src.summarizer import Summarizer
import sys

print("Testing Summarizer Class...")
try:
    s = Summarizer() # Should use default llama3.1
    print("Summarizer initialized.")
except Exception as e:
    print(f"Failed to init Summarizer: {e}")
    sys.exit(1)

text = "This is a test sentence to check if the summarizer works correctly. It should call Ollama and return a summary."
print(f"Summarizing text: {text}")
try:
    summary = s.summarize(text)
    print(f"Summary result: {summary}")
except Exception as e:
    print(f"Failed to summarize: {e}")
    sys.exit(1)
