#!/bin/bash

# Ensure we're in the correct directory
cd "$(dirname "$0")/src"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if required packages are installed
if ! python3 -c "import websockets, PIL" &> /dev/null; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
fi

# Run the WebSocket client
echo "Starting frame client..."
python3 main.py
