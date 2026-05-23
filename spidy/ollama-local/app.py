from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

OLLAMA_URL = "http://localhost:11434/api/generate"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("prompt", "")
    payload = {
        "model": "gemma:2b",  # or your model
        "prompt": user_input,
        "stream": True  # streaming enabled
    }

    # Call Ollama API with stream=True
    r = requests.post(OLLAMA_URL, json=payload, stream=True)

    def event_generator():
        for chunk in r.iter_content(chunk_size=None):
            if chunk:
                # Each chunk is bytes - decode and parse
                decoded = chunk.decode('utf-8')
                yield decoded

    return StreamingResponse(event_generator(), media_type="text/event-stream")
