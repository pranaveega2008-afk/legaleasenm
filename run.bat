@echo off
title LegalEase - AI Legal Document Generator
color 0b

echo ========================================================
echo         Welcome to LegalEase Generator
echo       (FastAPI Backend + Streamlit Frontend)
echo ========================================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not detected in your system PATH.
    echo.
    echo Please install Python 3.10+ from: https://www.python.org/downloads/
    echo **IMPORTANT**: Make sure to check the box:
    echo     "Add python.exe to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [1/3] Installing dependencies (using --user)...
python -m pip install --user -r requirements.txt
if %errorlevel% neq 0 (
    echo [WARNING] Could not install with --user, trying standard install...
    python -m pip install -r requirements.txt
)

echo.
echo [2/3] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "LegalEase Backend (FastAPI)" cmd /k "python -m uvicorn backend:app --host 127.0.0.1 --port 8000"

:: Wait 3 seconds for backend to initialize
timeout /t 3 /nobreak >nul

echo.
echo [3/3] Launching Streamlit Frontend...
echo Opening in your browser...
echo.
python -m streamlit run app.py

pause
