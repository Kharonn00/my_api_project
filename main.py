from fastapi import FastAPI, HTTPException, Query, Request
from pydantic import BaseModel
from typing import Optional
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Create rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI()

# Add rate limit error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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

# Root endpoint - Allow 10 requests per minute
@app.get("/")
@limiter.limit("10/minute")
def read_root(request: Request):
    return {"message": "Task Manager API - Go to /docs for documentation"}

# CREATE - Allow 5 new tasks per minute (prevent spam)
@app.post("/tasks/", response_model=Task)
@limiter.limit("5/minute")
def create_task(request: Request, task: Task):
    global task_id_counter
    task.id = task_id_counter
    task_id_counter += 1
    tasks.append(task.dict())
    return task

# READ all - Allow 20 requests per minute
@app.get("/tasks/")
@limiter.limit("20/minute")
def get_all_tasks(
    request: Request,
    search: Optional[str] = None,
    completed: Optional[bool] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = "asc",
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page (max 100)")
):
    """
    Get all tasks with optional filtering, sorting, and pagination
    """
    filtered_tasks = tasks.copy()
    
    # Filter by search query
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
    
    # Sort tasks
    if sort_by:
        reverse = (order == "desc")
        
        if sort_by == "title":
            filtered_tasks = sorted(filtered_tasks, key=lambda x: x["title"].lower(), reverse=reverse)
        elif sort_by == "id":
            filtered_tasks = sorted(filtered_tasks, key=lambda x: x["id"], reverse=reverse)
        elif sort_by == "completed":
            filtered_tasks = sorted(filtered_tasks, key=lambda x: x["completed"], reverse=reverse)
    
    # Pagination
    total_items = len(filtered_tasks)
    total_pages = (total_items + page_size - 1) // page_size
    
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    
    paginated_tasks = filtered_tasks[start_index:end_index]
    
    has_previous = page > 1
    has_next = page < total_pages
    
    return {
        "tasks": paginated_tasks,
        "pagination": {
            "current_page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_previous": has_previous,
            "has_next": has_next,
            "previous_page": page - 1 if has_previous else None,
            "next_page": page + 1 if has_next else None
        },
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

# DELETE - Allow 10 deletes per minute
@app.delete("/tasks/{task_id}")
@limiter.limit("10/minute")
def delete_task(request: Request, task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(index)
            return {"message": "Task deleted successfully", "deleted_task": deleted_task}
    raise HTTPException(status_code=404, detail="Task not found")

# UTILITY: Generate sample tasks for testing
@app.post("/tasks/generate-samples")
def generate_sample_tasks(count: int = Query(25, ge=1, le=100)):
    """
    Generate sample tasks for testing pagination
    """
    global task_id_counter
    
    generated = []
    for i in range(count):
        task = {
            "id": task_id_counter,
            "title": f"Sample Task {task_id_counter}",
            "description": f"This is test task number {task_id_counter}",
            "completed": task_id_counter % 3 == 0  # Every 3rd task is completed
        }
        
        tasks.append(task)
        generated.append(task)
        task_id_counter += 1
    
    return {
        "message": f"Generated {count} sample tasks",
        "generated": generated
    }  

# Railway to assign the port dynamically.
if __name__ == "__main__":
import uvicorn
import os
port = int(os.environ.get("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)