#!/bin/bash



set -e

URL="http://127.0.0.1:5000/api/timeline_post"

# generate random data
RAND_NUM=$RANDOM
NAME="Test User $RAND_NUM"
EMAIL="test$RAND_NUM@example.com"
CONTENT="Hello from test script $RAND_NUM"

echo ">>> Creating timeline post..."
POST_RESPONSE=$(curl -s -X POST "$URL" \
  -d "name=$NAME" \
  -d "email=$EMAIL" \
  -d "content=$CONTENT")

echo "POST response: $POST_RESPONSE"

# extract ID from POST response
POST_ID=$(echo "$POST_RESPONSE" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

echo ">>> Verifying timeline post with ID $POST_ID..."

GET_RESPONSE=$(curl -s "$URL")
echo "$GET_RESPONSE" | grep "$CONTENT" > /dev/null && echo "✓ Found post in GET response." || echo "✗ Post not found in GET response."

echo ">>> Cleaning up test post..."
DELETE_RESPONSE=$(curl -s -X DELETE "$URL/$POST_ID")
echo "DELETE response: $DELETE_RESPONSE"
