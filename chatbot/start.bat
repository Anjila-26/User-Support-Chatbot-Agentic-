@echo off
REM Customer Support AI System - Docker Startup Script for Windows

echo Starting Customer Support AI System...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not running. Please start Docker first.
    exit /b 1
)

REM Stop any running containers
echo Stopping any existing containers...
docker-compose down

REM Build and start services
echo Building and starting services...
docker-compose up --build -d

REM Wait for services to be ready
echo Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check health status
echo Checking service health...

REM Check backend
curl -f -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo Backend is healthy
) else (
    echo Backend health check failed
    docker-compose logs backend
    exit /b 1
)

REM Check frontend
curl -f -s http://localhost:8501/_stcore/health >nul 2>&1
if %errorlevel% equ 0 (
    echo Frontend is healthy
) else (
    echo Frontend health check failed
    docker-compose logs frontend
    exit /b 1
)

echo.
echo Customer Support AI System is running!
echo.
echo Frontend (Streamlit): http://localhost:8501
echo Backend API: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo To stop the system: docker-compose down
echo To view logs: docker-compose logs