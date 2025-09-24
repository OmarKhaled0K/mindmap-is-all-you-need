# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json

app = FastAPI(title="Mindmap API")

# Allow common local dev origins (Streamlit default runs on 8501)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for local dev; lock down for production
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "llm.json"

@app.get("/mindmap")
def get_mindmap():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Mindmap data not found.")
    return data

# Optional health endpoint
@app.get("/health")
def health():
    return {"status": "ok"}
