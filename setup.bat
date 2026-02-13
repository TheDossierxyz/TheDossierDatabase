@echo off
echo ===================================================
echo   Community Database - Contributor Setup Script
echo ===================================================

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b
)

:: Create Virtual Environment
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
) else (
    echo [INFO] Virtual environment already exists.
)

:: Activate venv and install requirements
echo [INFO] Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

:: Create .env if it doesn't exist
if not exist ".env" (
    echo [INFO] Creating .env file from template...
    type .env.example > .env
    echo [IMPORTANT] Please open .env and add your API Key!
    notepad .env
) else (
    echo [INFO] .env file already exists.
)

echo.
echo ===================================================
echo   Setup Complete! Launching Dashboard...
echo ===================================================
echo.

start "" "venv\Scripts\pythonw.exe" "src\dashboard.py"
