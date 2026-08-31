from fastapi import FastAPI
from datetime import datetime


app = FastAPI(
    title="MyAssistant Backend",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "assistant": "MyAssistant",
        "time": datetime.now().isoformat()
    }


@app.get("/")
def root():
    return {
        "message": "MyAssistant backend is running."
    }