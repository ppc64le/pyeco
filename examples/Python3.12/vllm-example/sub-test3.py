# fastapi_transformers_example.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from typing import Optional

app = FastAPI()

# Load a transformers pipeline for sentiment-analysis (lightweight and quick)
classifier = pipeline("sentiment-analysis")

class TextInput(BaseModel):
    text: str
    top_k: Optional[int] = 1  # number of top predictions

@app.post("/classify")
def classify(input: TextInput):
    if not input.text.strip():
        raise HTTPException(status_code=400, detail="Text must not be empty")

    results = classifier(input.text, top_k=input.top_k)
    return {"results": results}

# ----------- Simple Test -----------
if __name__ == "__main__":
    import uvicorn
    import requests
    import threading
    import time

    def run_server():
        uvicorn.run(app, host="127.0.0.1", port=8000)

    # Run FastAPI server in a background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait a moment for the server to start
    time.sleep(2)

    # Test data
    test_payload = {"text": "I love using transformers with FastAPI!", "top_k": 2}

    response = requests.post("http://127.0.0.1:8000/classify", json=test_payload)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
