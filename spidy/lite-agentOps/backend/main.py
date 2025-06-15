from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from models import Workflow
from executor import run_task
import os
import json
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

WORKFLOW_DIR = "./workflows"
OLLAMA_URL = "http://localhost:11434/api/generate"
if not os.path.exists(WORKFLOW_DIR):
    os.makedirs(WORKFLOW_DIR)

@app.get("/")
async def serve_index():
    return FileResponse("../frontend/index.html")

@app.get("/api/workflows")
def list_workflows():
    files = [f.replace(".json", "") for f in os.listdir(WORKFLOW_DIR) if f.endswith(".json")]
    return {"workflows": files}

@app.get("/api/workflows/{name}")
def get_workflow(name: str):
    path = f"{WORKFLOW_DIR}/{name}.json"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Workflow not found")
    with open(path) as f:
        return json.load(f)

@app.post("/api/workflows")
def save_workflow(workflow: Workflow):
    path = f"{WORKFLOW_DIR}/{workflow.name}.json"
    with open(path, "w") as f:
        json.dump(workflow.dict(), f, indent=2)
    return {"message": "Workflow saved successfully"}

@app.delete("/api/workflows/{name}")
def delete_workflow(name: str):
    path = f"{WORKFLOW_DIR}/{name}.json"
    if os.path.exists(path):
        os.remove(path)
        return {"message": "Workflow deleted"}
    raise HTTPException(status_code=404, detail="Workflow not found")

@app.post("/api/run-workflow/{name}")
def run_workflow(name: str):
    path = f"{WORKFLOW_DIR}/{name}.json"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Workflow not found")
    with open(path) as f:
        data = json.load(f)
    workflow = Workflow(**data)
    results = []
    for task in workflow.tasks:
        result = run_task(task)
        results.append({
            "command": task.command,
            "result": result
        })
    return {"workflow": workflow.name, "results": results}

@app.post("/api/run-workflow/{name}")
def run_workflow(name: str):
    path = f"{WORKFLOW_DIR}/{name}.json"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Workflow not found")
    with open(path) as f:
        data = json.load(f)
    workflow = Workflow(**data)
    output_text = ""
    for task in workflow.tasks:
        result = run_task(task)
        output_text += f"$ {task.command}\n{result}\n\n"
    return {"output": output_text.strip()}

OLLAMA_URL = "http://localhost:11434/api/generate"  # already running

from fastapi import Request, HTTPException
import requests, json, re

OLLAMA_URL = "http://localhost:11434/api/generate"

@app.post("/api/generate-workflow")
async def generate_workflow(request: Request):
    data = await request.json()
    user_prompt = data.get("prompt", "").strip()

    if not user_prompt:
        raise HTTPException(status_code=400, detail="Prompt required.")

    payload = {
        "model": "gemma:2b",
        "prompt": f"""
    You are a DevOps assistant integrated into a project called Lite AgentOps. This project allows users to create visual automation workflows using shell tasks.
    Your job is to take a user prompt and return a valid shell-based workflow in strict JSON format. The output will be directly parsed by a frontend and used in workflow automation.
    Your response must be:
    - Pure JSON (no markdown, no explanations)
    - Always follow the exact format below
    - Use only shell commands inside tasks
    - Each command must be a separate task in the "tasks" list. This is MUST follow. Do NOT use '&&' to combine commands.
    Format:
    {{
    "name": "meaningful-workflow-name",
    "tasks": [
        {{ "type": "shell", "command": "first command" }},
        {{ "type": "shell", "command": "second command" }}
    ]
    }}
    Important Rules:
    - Return only valid JSON.
    - Avoid duplicate tasks or unrelated commands.
    - Shell commands must be real and executable on Ubuntu/Debian systems.
    - Prefer common CLI tools (apt, curl, docker, systemctl, etc.).
    - NEVER include comments, markdown, or extra text.
    - dont use "&&" to add 2 commands
    User prompt: "{user_prompt}"
    """,
        "stream": False
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload)
        res.raise_for_status()
        raw = res.json().get("response", "").strip()
        print(" Raw AI response:\n", raw)

        # Extract JSON safely
        match = re.search(r'\{[\s\S]*\}', raw)  # match outermost JSON
        if not match:
            raise ValueError("No valid JSON found in AI response.")

        try:
            parsed_json = json.loads(match.group(0))
            # Extra validation: must have name + tasks[]
            if "name" not in parsed_json or not isinstance(parsed_json.get("tasks", None), list):
                raise ValueError("JSON missing 'name' or 'tasks' list.")
            return parsed_json
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")


    except Exception as e:
        print("❌ Error:", str(e))
        print(" Full response:", res.text if 'res' in locals() else "No response")
        raise HTTPException(status_code=500, detail=f"AI parsing failed: {str(e)}")
