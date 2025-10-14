# Task Manager API

A RESTful CRUD API built with FastAPI for managing tasks. This project demonstrates the fundamental operations of Create, Read, Update, and Delete (CRUD) with automatic data validation and interactive API documentation.

## Features

- ✅ **Create** new tasks with title, description, and completion status
- 📖 **Read** all tasks or retrieve individual tasks by ID
- ✏️ **Update** existing tasks
- 🗑️ **Delete** tasks permanently
- 🔍 Automatic data validation using Pydantic models
- 📚 Interactive API documentation (Swagger UI)
- ⚡ Fast and lightweight using FastAPI

## Technologies Used

- **Python 3.x**
- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - Lightning-fast ASGI server

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd my_api_project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API**
   - API: http://127.0.0.1:8000
   - Interactive Docs: http://127.0.0.1:8000/docs
   - Alternative Docs: http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| POST | `/tasks/` | Create a new task |
| GET | `/tasks/` | Get all tasks |
| GET | `/tasks/{task_id}` | Get a specific task by ID |
| PUT | `/tasks/{task_id}` | Update an existing task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Usage Examples

### Create a Task
```bash
POST /tasks/
{
  "title": "Learn FastAPI",
  "description": "Build a CRUD API",
  "completed": false
}
```

### Get All Tasks
```bash
GET /tasks/
```

### Update a Task
```bash
PUT /tasks/1
{
  "title": "Learn FastAPI - Updated",
  "description": "Build an awesome CRUD API",
  "completed": true
}
```

### Delete a Task
```bash
DELETE /tasks/1
```

## Data Model

```python
{
  "id": int,              # Auto-generated
  "title": str,           # Required
  "description": str,     # Optional
  "completed": bool       # Default: false
}
```

## What I Learned

- How to build RESTful APIs using FastAPI
- Implementing CRUD operations with HTTP methods (POST, GET, PUT, DELETE)
- Data validation and serialization with Pydantic models
- Using type hints for better code quality and automatic documentation
- Testing APIs with Swagger UI
- Understanding the relationship between APIs, frontends, and databases

## Future Improvements

- [ ] Connect to a persistent database (PostgreSQL/SQLite)
- [ ] Add user authentication and authorization
- [ ] Implement search and filtering functionality
- [ ] Add pagination for large datasets
- [ ] Deploy to cloud platform (AWS/Heroku/Railway)
- [ ] Add automated testing with pytest
- [ ] Implement sorting algorithms for task prioritization

## License

This project is open source and available for educational purposes.

## Contact

[Your Name] - [Your GitHub Profile] - [Your Email]

---

Built as part of my journey to becoming a Backend Python Developer 🚀
