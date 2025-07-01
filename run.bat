@echo off
REM AI Terminal Command Analyzer - Windows Runner

echo AI Terminal Command Analyzer
echo ===========================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo Error: .env file not found
    echo Please make sure the .env file exists with your Groq API key
    echo You can copy from .env.example and add your API key
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import groq, dotenv, requests, psutil" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Run the analyzer
echo Starting AI agent...
python main.py %*

if %errorlevel% neq 0 (
    echo.
    echo Error occurred. Check the output above for details.
    pause
)
