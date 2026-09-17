@echo off
setlocal
cd /d "%~dp0"

echo Checking for Python 3.10 or higher...
py -3 -c "import sys; assert sys.version_info >= (3,10)" 2>nul
if errorlevel 1 (
    echo.
    echo Python 3.10 or higher is required but was not found.
    echo Please install a newer version from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Creating virtual environment in neurodemo_venv...
py -3 -m venv neurodemo_venv

call neurodemo_venv\Scripts\activate.bat

echo Installing requirements...
pip install -r requirements.txt

echo.
echo Done! Double-click Run_this.bat to start the program.
pause
