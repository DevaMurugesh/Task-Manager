# main.py - FastAPI Backend Server
# This is the backend API that handles all database operations
# Using SQLite - no server installation needed!

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
from datetime import datetime
import os

# Create FastAPI app instance
app = FastAPI(title="Task Manager API")

# CORS Configuration - Allows React frontend to communicate with backend
# Without this, browsers will block requests from React (port 3000) to FastAPI (port 8000)
# Get allowed origins from environment variable (for Vercel deployment)
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Supports multiple origins (localhost + Vercel domain)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allows all headers
)

# Database Configuration - SQLite uses a file instead of a server
DB_FILE = os.getenv("DB_FILE", "task_manager.db")

# Initialize database - create table if it doesn't exist
def init_database():
    """Create the database file and table if they don't exist"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"Database initialized: {DB_FILE}")

# Initialize database on startup
init_database()

# Pydantic Models - These define the structure of data we send/receive
class TaskCreate(BaseModel):
    """Model for creating a new task"""
    title: str
    description: Optional[str] = None
    status: str = "pending"  # Default status

class TaskUpdate(BaseModel):
    """Model for updating an existing task"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class Task(BaseModel):
    """Model representing a complete task with all fields"""
    id: int
    title: str
    description: Optional[str]
    status: str
    created_at: str  # SQLite returns datetime as string

# Database Connection Function
def get_db_connection():
    """
    Creates and returns a SQLite database connection
    SQLite is file-based, so no server is needed!
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        # Set row factory to return rows as dictionaries
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Database connection error: {str(e)}"
        )

# Helper function to convert Row to dict
def row_to_dict(row):
    """Convert SQLite Row to dictionary"""
    return dict(row)

# API Endpoints (Routes)

@app.get("/")
def read_root():
    """Root endpoint - just a welcome message"""
    return {"message": "Welcome to Task Manager API"}

@app.get("/health")
def health_check():
    """Health check endpoint - tests database connection"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        conn.close()
        return {
            "status": "healthy",
            "database": "connected",
            "database_type": "SQLite",
            "database_file": DB_FILE,
            "message": "API and database are working correctly"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "message": "API is running but database connection failed"
        }

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    """
    GET /tasks - Retrieve all tasks from database
    Returns: List of all tasks
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        rows = cursor.fetchall()
        tasks = [row_to_dict(row) for row in rows]
        return tasks
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """
    GET /tasks/{task_id} - Retrieve a specific task by ID
    Path parameter: task_id
    Returns: Single task or 404 if not found
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
        if row is None:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return row_to_dict(row)
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    """
    POST /tasks - Create a new task
    Body: TaskCreate model (title, description, status)
    Returns: The created task with generated ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # SQL INSERT query with placeholders (?) for security (prevents SQL injection)
        cursor.execute(
            "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
            (task.title, task.description, task.status)
        )
        conn.commit()  # commit() saves changes to database
        
        # Get the ID of the newly created task
        task_id = cursor.lastrowid
        
        # Retrieve and return the complete task
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
        return row_to_dict(row)
    except sqlite3.Error as e:
        conn.rollback()  # rollback() undoes changes if error occurs
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    """
    PUT /tasks/{task_id} - Update an existing task
    Path parameter: task_id
    Body: TaskUpdate model (any fields to update)
    Returns: Updated task
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # First, check if task exists
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
        if row is None:
            raise HTTPException(status_code=404, detail="Task not found")
        
        existing_task = row_to_dict(row)
        
        # Build UPDATE query dynamically based on provided fields
        update_fields = []
        update_values = []
        
        if task_update.title is not None:
            update_fields.append("title = ?")
            update_values.append(task_update.title)
        
        if task_update.description is not None:
            update_fields.append("description = ?")
            update_values.append(task_update.description)
        
        if task_update.status is not None:
            update_fields.append("status = ?")
            update_values.append(task_update.status)
        
        if not update_fields:
            # No fields to update, return existing task
            return existing_task
        
        # Add updated_at timestamp
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        
        # Execute UPDATE query
        query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?"
        update_values.append(task_id)
        
        cursor.execute(query, tuple(update_values))
        conn.commit()
        
        # Retrieve and return updated task
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
        return row_to_dict(row)
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """
    DELETE /tasks/{task_id} - Delete a task
    Path parameter: task_id
    Returns: Success message
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if task exists
        cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
        if row is None:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Delete the task
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        
        return {"message": "Task deleted successfully"}
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()
