#!/bin/bash
cd "$(dirname "$0")"

if [ ! -f neurodemo_venv/bin/activate ]; then
    echo "Virtual environment not found. Please double-click Create_Env.command first."
    read -p "Press Enter to exit..."
    exit 1
fi

source neurodemo_venv/bin/activate
python neurodemo.py
read -p "Press Enter to close..."
