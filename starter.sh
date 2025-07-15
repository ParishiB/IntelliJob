#!/bin/bash

# Check if port 8000 is in use
if lsof -i :8000 >/dev/null; then
  echo "Port 8000 is in use. Killing the process..."
  fuser -k 8000/tcp
  echo "Process killed."
fi

# Run the python script
echo "Starting python script..."
python main.py

