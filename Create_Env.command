#!/bin/bash
cd "$(dirname "$0")"

echo "Checking for Python 3.10 or higher..."
if ! python3 -c "import sys; assert sys.version_info >= (3,10)" 2>/dev/null; then
    echo ""
    echo "Python 3.10 or higher is required but was not found."
    echo "Please install a newer version from https://www.python.org/downloads/"
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Creating virtual environment in neurodemo_venv..."
python3 -m venv neurodemo_venv || { read -p "Press Enter to exit..."; exit 1; }

source neurodemo_venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt || { read -p "Press Enter to exit..."; exit 1; }

echo ""
echo "Done! Double-click Run_this.command to start the program."
read -p "Press Enter to exit..."
