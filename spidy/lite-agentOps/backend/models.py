from pydantic import BaseModel
from typing import List, Literal, Optional

class Task(BaseModel):
    type: Literal["shell", "ansible"] = "shell"
    command: str
    name: Optional[str] = None  # for Ansible task name

class Workflow(BaseModel):
    name: str
    tasks: List[Task]

    def to_ansible_yaml(self) -> str:
        """Convert workflow to Ansible Playbook YAML"""
        playbook = [{
            "name": self.name,
            "hosts": "localhost",
            "become": True,
            "tasks": [
                {
                    "name": task.name or f"Run {task.command[:40]}",
                    "ansible.builtin.shell": task.command
                } for task in self.tasks
            ]
        }]
        import yaml
        return yaml.dump(playbook, sort_keys=False)
