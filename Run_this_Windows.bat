@echo off
setlocal
cd /d "%~dp0"

if not exist neurodemo_venv\Scripts\activate.bat (
    echo Virtual environment not found. Please double-click Create_Env_Windows.bat first.
    pause
    exit /b 1
)

call neurodemo_venv\Scripts\activate.bat
python neurodemo.py
if errorlevel 1 pause
