# Task Manager Backend - SQLite Version

## ✅ No Database Server Required!

This version uses **SQLite** instead of MySQL. SQLite is:
- ✅ **File-based** - No server installation needed
- ✅ **Zero configuration** - Works out of the box
- ✅ **Built into Python** - No extra packages needed
- ✅ **Perfect for development** - Simple and fast

## Quick Start

### 1. Install Dependencies

```bash
cd task-manager/backend
.\venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Mac/Linux

pip install -r requirements.txt
```

### 2. Start the Server

```bash
uvicorn main:app --reload --port 8000
```

That's it! The database will be created automatically when you first run the server.

## How It Works

- The database is stored in a file: `task_manager.db` (in the backend folder)
- The table is created automatically on first run
- No MySQL server needed!
- No passwords or configuration needed!

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check (shows database status)
- `GET /tasks` - Get all tasks
- `GET /tasks/{task_id}` - Get a specific task
- `POST /tasks` - Create a new task
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

## Database File Location

The database file `task_manager.db` will be created in:
```
task-manager/backend/task_manager.db
```

You can:
- **Backup**: Just copy the `.db` file
- **Reset**: Delete the `.db` file and restart the server
- **View**: Use any SQLite browser tool (like DB Browser for SQLite)

## Troubleshooting

### Database file not created?
- Make sure the backend folder is writable
- Check that the server started without errors

### Want to reset the database?
- Stop the server
- Delete `task_manager.db`
- Restart the server (it will recreate the database)

### Want to view/edit the database?
- Download DB Browser for SQLite: https://sqlitebrowser.org/
- Open `task_manager.db` file

## Migration from MySQL

If you had MySQL before:
- ✅ No need to migrate data (start fresh with SQLite)
- ✅ All your API endpoints work the same
- ✅ Frontend code doesn't need any changes
- ✅ Just restart the server and it works!












