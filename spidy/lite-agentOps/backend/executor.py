import subprocess
from models import Task

def run_task(task: Task):
    if task.type == "shell":
        try:
            result = subprocess.run(
                task.command, shell=True, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            return {"success": True, "output": result.stdout}
        except subprocess.CalledProcessError as e:
            return {"success": False, "output": e.stderr}
    else:
        return {"success": False, "output": "Unsupported task type"}
