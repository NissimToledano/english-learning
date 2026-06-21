@echo off
echo Starting English Learning Server...
cd /d "%~dp0"

REM Kill any process using port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 "') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo Server starting at http://localhost:8000
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
