#!/bin/bash

PROJECT_DIR=/root/projects/mlh-portfolio
VENV_DIR=$PROJECT_DIR/venv

echo "cd into project folder..."
cd "$PROJECT_DIR" || { echo "Failed to cd into $PROJECT_DIR"; exit 1; }

echo "fetching latest changes from GitHub..."
git fetch && git reset origin/main --hard

echo "checking virtual environment directory..."
if [ ! -f "$VENV_DIR/bin/activate" ]; then
  echo "Virtual environment activation script not found at $VENV_DIR/bin/activate"
  exit 1
fi

echo "activating virtual environment and installing dependencies..."
source "$VENV_DIR/bin/activate"

# Check if pip exists now
if ! command -v pip &> /dev/null; then
  echo "pip command not found after activating virtualenv"
  exit 1
fi

pip install -r requirements.txt

echo "restarting myportfolio service..."
sudo systemctl restart myportfolio

echo "checking service status..."
sudo systemctl status myportfolio --no-pager

echo "finished!"