from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

class Task(BaseModel):
    title: str
    description: str
    status: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

tasks = {}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return list(tasks.values())

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    task_id = str(uuid4())
    tasks[task_id] = task
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task_update: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    stored_task = tasks[task_id].dict()
    updated_data = task_update.dict(exclude_unset=True)
    stored_task.update(updated_data)
    tasks[task_id] = Task(**stored_task)
    return tasks[task_id]

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return {"message": "Task deleted"}
