import requests
import sys

print("Testing requests...")
try:
    print(f"requests version: {requests.__version__}")
except Exception as e:
    print(f"requests module issue: {e}")
    sys.exit(1)

print("\nTesting Ollama connection...")
url = "http://localhost:11434"
try:
    resp = requests.get(url, timeout=5)
    print(f"Ollama Status: {resp.status_code}")
    print("Ollama is running!")
except Exception as e:
    print(f"Failed to connect to Ollama: {e}")
    print("Make sure Ollama is running.")
