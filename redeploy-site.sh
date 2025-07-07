#!/bin/bash

PROJECT_DIR=/root/projects/mlh-portfolio
VENV_DIR=$PROJECT_DIR/venv

echo "killing all existing tmux sessions..."
tmux kill-server 2>/dev/null

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


if ! command -v pip &> /dev/null; then
  echo "pip command not found after activating virtualenv"
  exit 1
fi

pip install -r requirements.txt

echo "starting new tmux session running Flask server..."
tmux new -d -s flask-server "
  cd '$PROJECT_DIR'
  source '$VENV_DIR/bin/activate'
  flask run --host=0.0.0.0
"

echo "finished!"