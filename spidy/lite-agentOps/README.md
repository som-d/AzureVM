# Lite AgentOps — AI-Assisted Automation Platform

Local, privacy-focused platform that turns natural language into executable **Ansible Playbooks** using a local LLM (Ollama + Gemma 2B).

> Built for infra tasks like `Install Nginx and Start Service` — no cloud API key needed.

### Features
- **Visual Workflow Manager** — create, edit, save, load, delete workflows
- **AI Generation** — prompt like `Install Docker and start service` → generates shell tasks via Gemma 2B
- **Ansible Export** — one-click export any workflow as real Ansible Playbook YAML (`ansible.builtin.shell`) via `GET /api/workflows/{name}/ansible`
- **Sequential Execution** — runs tasks via `subprocess` and streams output
- **Local LLM** — Ollama `gemma:2b` at `http://localhost:11434`, no API costs, fully private
- **File-based Storage** — workflows saved as `backend/workflows/*.json`

### Architecture
 Browser / index.html  --prompt-->  FastAPI /api/generate-workflow  -->  Ollama gemma:2b  --> {name, tasks: {type:"ansible", command}}
 Browser  --save/load/run/export-->  FastAPI /api/workflows  -->  backend/workflows/*.json  -->  executor.py -> subprocess / ansible-playbook 

### Tech Stack
- **Backend:** Python, FastAPI, Pydantic, PyYAML, Requests
- **Frontend:** HTML, CSS, Vanilla JS
- **AI:** Ollama, Gemma 2B
- **Automation:** Shell + Ansible (`ansible.builtin.shell`)

### Quick Start
```bash
# 1. Backend
cd spidy/lite-agentOps/backend
pip install fastapi uvicorn requests pydantic pyyaml
ollama pull gemma:2b
ollama serve # keep running in another terminal
uvicorn main:app --reload --port 8000

# 2. Frontend
# Open http://localhost:8000/  (served by FastAPI)
# API docs: http://localhost:8000/docs
Usage
1. Enter AI Prompt: Install Nginx and Start Service → Click Generate with AI
2. Edit commands if needed → Click Save Workflow
3. Click Export as Ansible Playbook → downloads Install Nginx and Start Service.yml
4. Run: ansible-playbook "Install Nginx and Start Service.yml" or click Run Workflow to run directly
API
- GET /api/workflows — list workflows
- GET /api/workflows/{name} — get workflow JSON
- POST /api/workflows — save {name, tasks:[{type:"ansible", command, name}]}
- DELETE /api/workflows/{name}
- POST /api/run-workflow/{name} — execute sequentially
- POST /api/generate-workflow — {prompt:"..."} → {name, tasks}
- GET /api/workflows/{name}/ansible — export as Ansible YAML {name, yaml}
Project Structure
lite-agentOps/
├── backend/
│   ├── main.py          # FastAPI + Ollama + Ansible export
│   ├── executor.py      # shell/ansible runner
│   ├── models.py        # Task/Workflow + to_ansible_yaml()
│   └── workflows/       # *.json saved workflows
├── frontend/
│   ├── index.html       # UI with Export button
│   ├── style.css
│   └── script.js
└── docker-compose.yml   # TODO
Example Exported Playbook
- name: Nginx Setup
  hosts: localhost
  become: true
  tasks:
    - name: Run sudo apt update
      ansible.builtin.shell: sudo apt update
    - name: Run sudo apt install -y nginx
      ansible.builtin.shell: sudo apt install -y nginx
    - name: Run sudo systemctl start nginx
      ansible.builtin.shell: sudo systemctl start nginx
Author: Soham Deshmukh — DevOps Engineer | 2025
