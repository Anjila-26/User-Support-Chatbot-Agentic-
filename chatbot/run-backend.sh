#!/bin/bash
echo "Starting Customer Support Backend..."
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000