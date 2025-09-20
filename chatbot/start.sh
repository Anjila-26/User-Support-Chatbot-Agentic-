#!/bin/bash

# Customer Support AI System - Docker Startup Script
echo "🚀 Starting Customer Support AI System..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed."
    exit 1
fi

# Stop any running containers
echo "🛑 Stopping any existing containers..."
docker-compose down

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check health status
echo "🔍 Checking service health..."

# Check backend
if curl -f -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    docker-compose logs backend
    exit 1
fi

# Check frontend
if curl -f -s http://localhost:8501/_stcore/health > /dev/null; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed"
    docker-compose logs frontend
    exit 1
fi

echo ""
echo "🎉 Customer Support AI System is running!"
echo ""
echo "📱 Frontend (Streamlit): http://localhost:8501"
echo "🔧 Backend API: http://localhost:8000"
echo "📖 API Documentation: http://localhost:8000/docs"
echo ""
echo "To stop the system: docker-compose down"
echo "To view logs: docker-compose logs"