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

def bubble_sort_tasks(task_list, key_field):
    """
    Bubble Sort implementation - O(n²) time complexity
    Good for learning, bad for production (but perfect for interviews!)
    """
    n = len(task_list)
    sorted_list = task_list.copy()
    
    # Bubble Sort algorithm
    for i in range(n):
        # Track if we made any swaps
        swapped = False
        
        for j in range(0, n - i - 1):
            # Compare adjacent elements
            if sorted_list[j][key_field] > sorted_list[j + 1][key_field]:
                # Swap if they're in wrong order
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
                swapped = True
        
        # If no swaps were made, the list is already sorted
        if not swapped:
            break
    
    return sorted_list

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
def get_all_tasks(
    search: Optional[str] = None,
    completed: Optional[bool] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = "asc"
):
    """
    Get all tasks with optional filtering and sorting:
    - search: Search for tasks by title (case-insensitive)
    - completed: Filter by completion status (true/false)
    - sort_by: Sort by field (title, id, completed)
    - order: Sort order (asc for ascending, desc for descending)
    """
    filtered_tasks = tasks.copy()
    
    # Filter by search query (Linear Search Algorithm)
    if search:
        search_lower = search.lower()
        filtered_tasks = [
            task for task in filtered_tasks 
            if search_lower in task["title"].lower()
        ]
    
    # Filter by completion status
    if completed is not None:
        filtered_tasks = [
            task for task in filtered_tasks 
            if task["completed"] == completed
        ]
    
    # Sort tasks (Python's Timsort - a hybrid of Merge Sort and Insertion Sort)
    if sort_by:
        reverse = (order == "desc")
        
        if sort_by == "title":
            filtered_tasks = sorted(filtered_tasks, key=lambda x: x["title"].lower(), reverse=reverse)
        elif sort_by == "id":
            filtered_tasks = sorted(filtered_tasks, key=lambda x: x["id"], reverse=reverse)
        elif sort_by == "completed":
            filtered_tasks = sorted(filtered_tasks, key=lambda x: x["completed"], reverse=reverse)
    
    return {
        "tasks": filtered_tasks, 
        "total": len(filtered_tasks),
        "filters_applied": {
            "search": search,
            "completed": completed,
            "sort_by": sort_by,
            "order": order
        }
    }

# Special endpoint to demonstrate Bubble Sort algorithm
@app.get("/tasks/bubble-sort")
def get_tasks_bubble_sorted(sort_by: str = "id"):
    """
    Demonstrates Bubble Sort algorithm (O(n²) complexity)
    Educational endpoint - shows different sorting algorithms
    """
    if sort_by not in ["id", "title", "completed"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by field")
    
    sorted_tasks = bubble_sort_tasks(tasks, sort_by)
    
    return {
        "tasks": sorted_tasks,
        "total": len(sorted_tasks),
        "algorithm_used": "Bubble Sort",
        "time_complexity": "O(n²)",
        "note": "This is for educational purposes. Production uses Timsort (O(n log n))"
    }

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