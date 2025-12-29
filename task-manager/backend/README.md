# Task Manager Backend API

FastAPI backend server for the Task Manager application using SQLite.

## Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)
- **No database server installation needed!** (SQLite is file-based)

## Quick Start

### 1. Install Dependencies

```bash
# Activate virtual environment (if using one)
# On Windows:
.\venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. Start the Server

```bash
# Make sure you're in the backend directory
cd backend

# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### 3. Verify It's Working

Open your browser and visit:
- http://localhost:8000 - Should show `{"message": "Welcome to Task Manager API"}`
- http://localhost:8000/health - Should show database status
- http://localhost:8000/docs - Should show the interactive API documentation

## Database

This project uses **SQLite**, which means:
- ✅ No server installation needed
- ✅ Database is stored in a file: `task_manager.db`
- ✅ Table is created automatically on first run
- ✅ Zero configuration required

The database file will be created automatically in the `backend` directory when you first start the server.

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check (shows database status)
- `GET /tasks` - Get all tasks
- `GET /tasks/{task_id}` - Get a specific task
- `POST /tasks` - Create a new task
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

## Troubleshooting

### Port Already in Use
- If port 8000 is already in use, change it:
  ```bash
  uvicorn main:app --reload --port 8001
  ```
- Then update the `API_URL` in the frontend `App.js` to match

### CORS Errors
- Make sure the frontend is running on `http://localhost:3000`
- Check that CORS middleware is properly configured in `main.py`

### Database Issues
- The database file `task_manager.db` is created automatically
- To reset: Delete `task_manager.db` and restart the server
- To view/edit: Use DB Browser for SQLite (https://sqlitebrowser.org/)

## Development

The server runs with auto-reload enabled, so changes to `main.py` will automatically restart the server.
