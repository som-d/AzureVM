from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from models import Workflow
from executor import run_task
import os
import json
import requests
import re

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

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
    output_text = ""
    for task in workflow.tasks:
        result = run_task(task)
        output_text += f"$ {task.command}\n{result['output']}\n\n"
    return {"output": output_text.strip()}

# --- NEW: Ansible Playbook Generation ---
@app.post("/api/generate-workflow")
async def generate_workflow(request: Request):
    data = await request.json()
    user_prompt = data.get("prompt", "").strip()
    if not user_prompt:
        raise HTTPException(status_code=400, detail="Prompt required.")

    payload = {
        "model": "gemma:2b",
        "prompt": f"""
You are a DevOps assistant for Lite AgentOps. Convert user prompt into Ansible playbook tasks.
Your response must be pure JSON, no markdown, no explanation. Each shell command must be a separate task.
Format:
{{
  "name": "meaningful-workflow-name",
  "tasks": [
    {{ "type": "ansible", "command": "first shell command", "name": "what this does" }},
    {{ "type": "ansible", "command": "second shell command", "name": "what this does" }}
  ]
}}
Rules: Real executable Ubuntu/Debian commands only, use apt/curl/docker/systemctl, never combine with &&, return only JSON.
User prompt: "{user_prompt}"
""",
        "stream": False
    }
    try:
        res = requests.post(OLLAMA_URL, json=payload)
        res.raise_for_status()
        raw = res.json().get("response", "").strip()
        match = re.search(r'\{{[\s\S]*\}}', raw)
        if not match:
            raise ValueError("No valid JSON found in AI response.")
        parsed_json = json.loads(match.group(0))
        if "name" not in parsed_json or not isinstance(parsed_json.get("tasks", None), list):
            raise ValueError("JSON missing 'name' or 'tasks' list.")
        # Save workflow as JSON (still JSON, but now type=ansible)
        return parsed_json
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI parsing failed: {str(e)}")

@app.get("/api/workflows/{name}/ansible")
def get_ansible_playbook(name: str):
    """Export workflow as real Ansible YAML"""
    path = f"{WORKFLOW_DIR}/{name}.json"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Workflow not found")
    with open(path) as f:
        workflow = Workflow(**json.load(f))
    yaml_content = workflow.to_ansible_yaml()
    return {"name": f"{name}.yml", "yaml": yaml_content}
