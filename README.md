# Task Manager API 🚀

**🌐 Live Demo:** [Here.](https://myapiproject-production.up.railway.app/docs)

A production-ready RESTful CRUD API built with FastAPI, featuring advanced search, filtering, sorting, pagination, and rate limiting. This project demonstrates fundamental algorithms, data structures, and API design patterns used in modern backend systems.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Deployed on Railway](https://img.shields.io/badge/Deployed%20on-Railway-blueviolet.svg)](https://railway.app/)

---

## ✨ Features

### Core CRUD Operations
- ✅ **Create** new tasks with title, description, and completion status
- 📖 **Read** all tasks or retrieve individual tasks by ID
- ✏️ **Update** existing tasks with full data validation
- 🗑️ **Delete** tasks permanently

### Advanced Features
- 🔍 **Search** - Case-insensitive search by task title (Linear Search: O(n))
- 🎯 **Filter** - Filter tasks by completion status
- 📊 **Sort** - Multi-field sorting (title, ID, completion status) with ascending/descending order
- 📄 **Pagination** - Efficient data handling with customizable page sizes (offset-based pagination)
- 🛡️ **Rate Limiting** - API abuse prevention using Token Bucket Algorithm
  - Root endpoint: 10 requests/minute
  - Create tasks: 5 requests/minute  
  - Read tasks: 20 requests/minute
  - Delete tasks: 10 requests/minute
- 🔄 **Combined Operations** - Use search, filter, sort, and pagination together
- 🧮 **Algorithm Comparison** - Side-by-side demo of Timsort O(n log n) vs Bubble Sort O(n²)

### Technical Features
- 🔒 Automatic data validation using Pydantic models
- 📚 Interactive API documentation (Swagger UI & ReDoc)
- ⚡ Fast and lightweight using FastAPI
- 🎓 Educational endpoints demonstrating algorithms
- 🌐 Deployed and production-ready on Railway

---

## 🛠️ Technologies Used

- **Python 3.12** - Core programming language
- **FastAPI** - Modern, high-performance web framework
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - Lightning-fast ASGI server
- **SlowAPI** - Rate limiting middleware
- **Railway** - Cloud deployment platform

---

## 📋 Algorithms & Data Structures

| Algorithm | Type | Time Complexity | Space Complexity | Implementation |
|-----------|------|-----------------|------------------|----------------|
| **Linear Search** | Searching | O(n) | O(1) | Text search in task titles |
| **Timsort** | Sorting | O(n log n) | O(n) | Python's default sort (production) |
| **Bubble Sort** | Sorting | O(n²) | O(1) | Educational demonstration |
| **Offset Pagination** | Data Retrieval | O(1) | O(k) | Efficient large dataset handling |
| **Token Bucket** | Rate Limiting | O(1) | O(n) | API abuse prevention |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Local Installation

1. **Clone the repository**
git clone https://github.com/Kharonn00/my_api_project.git
cd my_api_project

text

2. **Create and activate virtual environment**
Create venv
python -m venv venv

Activate (macOS/Linux)
source venv/bin/activate

Activate (Windows)
.\venv\Scripts\activate

text

3. **Install dependencies**
pip install -r requirements.txt

text

4. **Run the application**
uvicorn main:app --reload

text

5. **Access the API**
- 🏠 API Root: http://127.0.0.1:8000
- 📖 Swagger UI: http://127.0.0.1:8000/docs
- 📋 ReDoc: http://127.0.0.1:8000/redoc

---

## 📡 API Endpoints

### Core CRUD Operations

| Method | Endpoint | Description | Rate Limit |
|--------|----------|-------------|------------|
| GET | `/` | Welcome message and API info | 10/min |
| POST | `/tasks/` | Create a new task | 5/min |
| GET | `/tasks/` | Get all tasks (with filters/pagination) | 20/min |
| GET | `/tasks/{task_id}` | Get a specific task by ID | - |
| PUT | `/tasks/{task_id}` | Update an existing task | - |
| DELETE | `/tasks/{task_id}` | Delete a task | 10/min |

### Utility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks/bubble-sort` | Get tasks sorted using Bubble Sort O(n²) |
| POST | `/tasks/generate-samples` | Generate sample tasks for testing |

### Query Parameters (GET /tasks/)

| Parameter | Type | Default | Description | Example |
|-----------|------|---------|-------------|---------|
| `search` | string | None | Search by title (case-insensitive) | `?search=python` |
| `completed` | boolean | None | Filter by completion status | `?completed=true` |
| `sort_by` | string | None | Sort field (title/id/completed) | `?sort_by=title` |
| `order` | string | asc | Sort order (asc/desc) | `?order=desc` |
| `page` | integer | 1 | Page number (min: 1) | `?page=2` |
| `page_size` | integer | 10 | Items per page (min: 1, max: 100) | `?page_size=20` |

---

## 💡 Usage Examples

### Create a Task
POST /tasks/
Content-Type: application/json

{
"title": "Learn FastAPI",
"description": "Build a production-ready CRUD API",
"completed": false
}

text

**Response:**
{
"id": 1,
"title": "Learn FastAPI",
"description": "Build a production-ready CRUD API",
"completed": false
}

text

### Search & Filter with Pagination
GET /tasks/?search=Learn&completed=false&page=1&page_size=10

text

**Response:**
{
"tasks": [...],
"pagination": {
"current_page": 1,
"page_size": 10,
"total_items": 25,
"total_pages": 3,
"has_previous": false,
"has_next": true,
"next_page": 2
},
"filters_applied": {
"search": "Learn",
"completed": false,
"sort_by": null,
"order": "asc"
}
}

text

### Sort Tasks by Title (Descending)
GET /tasks/?sort_by=title&order=desc

text

### Combine All Features
GET /tasks/?search=API&completed=false&sort_by=title&order=asc&page=1&page_size=5

text
*Returns incomplete tasks containing "API", sorted alphabetically, showing first 5 results*

### Compare Sorting Algorithms
Using Timsort (default, O(n log n))
GET /tasks/?sort_by=id

Using Bubble Sort (educational, O(n²))
GET /tasks/bubble-sort?sort_by=id

text

### Generate Test Data
POST /tasks/generate-samples?count=50

text
*Creates 50 sample tasks for testing pagination*

---

## 📊 Data Model

{
"id": int, # Auto-generated unique identifier
"title": str, # Required, task name (1-200 chars)
"description": str, # Optional, task details
"completed": bool # Default: false, completion status
}

text

---

## 🧠 What I Learned

### Backend Development Concepts
- RESTful API design principles and best practices
- CRUD operations with proper HTTP method usage
- Query parameter handling for complex filtering
- Request validation and error handling
- Rate limiting strategies for API security
- Production deployment on cloud platforms

### Algorithms & Time Complexity
- **Linear Search** - O(n) for text matching in arrays
- **Sorting Algorithms** - Trade-offs between O(n²) and O(n log n)
  - Bubble Sort: Simple but inefficient for large datasets
  - Timsort: Hybrid approach combining Merge Sort and Insertion Sort
- **Pagination Algorithm** - Offset calculation: `start = (page - 1) × page_size`
- **Token Bucket Algorithm** - Rate limiting with O(1) check time
- **Big O Notation** - Analyzing and optimizing algorithm performance

### Software Engineering Practices
- Type hints and Pydantic models for type safety
- Virtual environments for dependency isolation
- Git version control and GitHub workflows
- Writing professional documentation
- Environment-based configuration for deployment
- API security patterns (rate limiting, validation)

---

## 🎯 Interview Talking Points

This project demonstrates:
- ✅ **API Design** - RESTful principles, pagination, filtering, sorting
- ✅ **Algorithm Implementation** - Search and sort with complexity analysis
- ✅ **Data Structures** - Efficient use of lists, dictionaries, and indexing
- ✅ **System Design** - Rate limiting, validation, error handling
- ✅ **Production Skills** - Deployment, environment config, documentation

## 🚧 Future Enhancements

**Phase 1: Database Integration**
- [ ] Connect to PostgreSQL for persistent storage
- [ ] Implement database migrations with Alembic
- [ ] Add database indexing for O(1) lookups

**Phase 2: Authentication & Security**
- [ ] JWT token-based authentication
- [ ] User registration and login
- [ ] Role-based access control (RBAC)
- [ ] API key management

**Phase 3: Advanced Features**
- [ ] Task dependencies using Directed Acyclic Graphs (DAG)
- [ ] Topological sorting for dependency resolution
- [ ] Task priority system with Min Heap data structure
- [ ] Full-text search with fuzzy matching
- [ ] WebSocket support for real-time updates

**Phase 4: Performance & Scale**
- [ ] Redis caching for frequently accessed data
- [ ] Database query optimization
- [ ] Load testing and performance benchmarks
- [ ] Horizontal scaling with load balancers

**Phase 5: DevOps & Testing**
- [ ] Automated testing with pytest (unit + integration)
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Docker containerization
- [ ] Monitoring and logging (Sentry, DataDog)

---

## 📈 Performance Considerations

### Current Implementation
- **Storage**: In-memory Python list (resets on restart)
- **Search**: O(n) linear search through all tasks
- **Sort**: O(n log n) using Python's Timsort
- **Pagination**: O(1) slice operation after filtering
- **Best for**: Small to medium datasets (< 10,000 tasks)

### Production Optimizations
- **Database indexes** for O(1) lookup by ID
- **Full-text search engines** (Elasticsearch) for complex queries
- **Caching layer** (Redis) for frequently accessed data
- **Pagination** with database-level LIMIT/OFFSET
- **Async operations** for I/O-bound tasks

---

## 🤝 Contributing

This is an educational project, but feedback is welcome! Feel free to:
- Open issues for bugs or suggestions
- Fork and submit pull requests
- Share your own implementations

---

## 📝 License

This project is open source and available for educational purposes.

---

## 📬 Contact

**Ariel Espinal**  
📧 Email: ariel.espinal09@gmail.com  
💼 LinkedIn: [https://linkedin.com/in/yourprofile](https://www.linkedin.com/in/aespi09/)
🐙 GitHub: [@Kharonn00](https://github.com/Kharonn00)

---

**Built with ❤️ as part of my journey to becoming a Backend Developer**

*Demonstrating CRUD operations, search algorithms, sorting algorithms, pagination, rate limiting, and RESTful API design*

**⭐ If you found this project helpful, please give it a star!**
