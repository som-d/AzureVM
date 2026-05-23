from pydantic import BaseModel
from typing import List, Literal

class Task(BaseModel):
    type: Literal["shell"]  # we support only shell for now
    command: str

class Workflow(BaseModel):
    name: str
    tasks: List[Task]
