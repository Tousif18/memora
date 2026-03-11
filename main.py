from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Memora backend running successfully"}

@app.get("/chat")
def chat(q: str):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi",
            "prompt": f"You are Memora, a gentle elderly care assistant. Reply warmly and simply: {q}",
            "stream": False
     }
    )
    return response.json()