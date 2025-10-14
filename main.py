from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# This is our data model - it defines what a task looks like
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

# In-memory "database" (just a list for now)
tasks = []
task_id_counter = 1

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Task Manager API - Go to /docs for documentation"}

# CREATE: Add a new task
@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    global task_id_counter
    task.id = task_id_counter
    task_id_counter += 1
    tasks.append(task.dict())
    return task

# READ: Get all tasks
@app.get("/tasks/")
def get_all_tasks():
    return {"tasks": tasks, "total": len(tasks)}

# READ: Get a specific task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# UPDATE: Modify an existing task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            # Keep the same ID but update everything else
            updated_task.id = task_id
            tasks[index] = updated_task.dict()
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

# DELETE: Remove a task completely
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(index)
            return {"message": "Task deleted successfully", "deleted_task": deleted_task}
    raise HTTPException(status_code=404, detail="Task not found")