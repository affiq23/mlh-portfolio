#!/bin/bash

PROJECT_DIR=/root/projects/mlh-portfolio

echo "cd into project folder..."
cd "$PROJECT_DIR" || { echo "Failed to cd into $PROJECT_DIR"; exit 1; }

echo "fetching latest changes from GitHub..."
git fetch && git reset origin/main --hard

echo "stopping containers to prevent memory issues during build..."
docker compose -f docker-compose.prod.yml down

echo "rebuilding and starting containers..."
docker compose -f docker-compose.prod.yml up -d --build

echo "checking container status..."
docker compose -f docker-compose.prod.yml ps

echo "finished!"