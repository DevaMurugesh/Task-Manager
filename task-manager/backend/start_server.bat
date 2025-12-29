@echo off
echo Starting Task Manager Backend Server...
echo.
echo Make sure MySQL is running and database is set up!
echo.
cd /d %~dp0
.\venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause












