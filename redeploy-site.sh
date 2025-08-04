#!/bin/bash

PROJECT_DIR=/root/projects/mlh-portfolio

echo "=== Safe Deployment Script ==="
echo "Checking system resources..."

# Check available memory
AVAILABLE_MEM=$(free -m | awk 'NR==2{printf "%.0f", $7}')
echo "Available memory: ${AVAILABLE_MEM}MB"

if [ "$AVAILABLE_MEM" -lt 200 ]; then
    echo "WARNING: Low memory detected. Consider stopping other services first."
    echo "Continue anyway? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Deployment cancelled."
        exit 1
    fi
fi

echo "Changing to project directory..."
cd "$PROJECT_DIR" || { echo "Failed to cd into $PROJECT_DIR"; exit 1; }

echo "Fetching latest changes from GitHub..."
git fetch && git reset origin/main --hard

echo "Stopping existing containers..."
docker compose -f docker-compose.prod.yml down

echo "Cleaning up unused Docker resources..."
docker system prune -f

echo "Building application (this may take a while)..."
docker compose -f docker-compose.prod.yml build myportfolio

echo "Starting MySQL database..."
docker compose -f docker-compose.prod.yml up -d mysql

echo "Waiting for MySQL to be healthy..."
timeout=300  # 5 minutes
elapsed=0
while [ $elapsed -lt $timeout ]; do
    if docker compose -f docker-compose.prod.yml ps mysql | grep -q "healthy"; then
        echo "MySQL is ready!"
        break
    fi
    echo "Waiting for MySQL... (${elapsed}s elapsed)"
    sleep 10
    elapsed=$((elapsed + 10))
done

if [ $elapsed -ge $timeout ]; then
    echo "ERROR: MySQL failed to start within 5 minutes"
    docker compose -f docker-compose.prod.yml logs mysql
    exit 1
fi

echo "Starting application..."
docker compose -f docker-compose.prod.yml up -d myportfolio

echo "Starting nginx..."
docker compose -f docker-compose.prod.yml up -d nginx

echo "Checking final status..."
docker compose -f docker-compose.prod.yml ps

echo "Checking resource usage..."
free -h
docker stats --no-stream

echo "=== Deployment Complete ==="
echo "site should be available at: https://affiq-site.duckdns.org"