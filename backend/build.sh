#!/usr/bin/env bash
# exit on error
set -o errexit

# Auto-detect if we are inside backend/ or root directory
if [ -d "../frontend" ]; then
    echo "Detected running from backend subdirectory. Moving to project root..."
    cd ..
fi

echo "=== Building React Frontend ==="
cd frontend
npm install
npm run build

echo "=== Building FastAPI Backend ==="
cd ../backend
pip install -r requirements.txt

echo "=== Build Completed Successfully ==="
