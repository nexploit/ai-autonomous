from fastapi import FastAPI
import threading
from loop import loop
from db import add_task

app = FastAPI(
    title="AI Cluster API",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/task")
def task(data: dict):
    add_task(data["task"])
    return {"status": "added"}

@app.on_event("startup")
def startup():
    threading.Thread(target=loop, daemon=True).start()