import subprocess
import os
import tempfile
from models import Task

def run_task(task: Task):
    if task.type in ["shell", "ansible"]:
        try:
            # Ansible tasks are just shell via ansible.builtin.shell,
            # so we execute the shell command directly (or via ansible if available)
            result = subprocess.run(
                task.command, shell=True, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            return {"success": True, "output": result.stdout}
        except subprocess.CalledProcessError as e:
            return {"success": False, "output": e.stderr}
    else:
        return {"success": False, "output": "Unsupported task type"}

def run_ansible_playbook(yaml_content: str):
    """Save YAML and run via ansible-playbook if available, else fallback"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write(yaml_content)
        f.flush()
        try:
            # Try ansible-playbook if installed
            result = subprocess.run(
                f"ansible-playbook {f.name}", shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Ansible not installed, YAML saved at {f.name}: {str(e)}"
        finally:
            os.unlink(f.name)
