#!/bin/bash
echo "Starting Task Manager Backend Server..."
echo ""
echo "Make sure MySQL is running and database is set up!"
echo ""
cd "$(dirname "$0")"
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000












