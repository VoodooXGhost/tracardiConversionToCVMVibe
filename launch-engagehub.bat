@echo off
title EngageHub CVM Platform - Docker Launcher

echo.
echo ========================================
echo    EngageHub CVM Platform Launcher
echo    Customer Value Management for Tmcel
echo ========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running or not installed!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo OK: Docker is running
echo.

REM Check if this is first run
if not exist ".docker-initialized" (
    echo SETUP: First time setup - This may take a few minutes...
    echo.
    
    echo BUILD: Building Docker images...
    docker-compose build
    
    if %errorlevel% neq 0 (
        echo ERROR: Failed to build Docker images
        pause
        exit /b 1
    )
    
    echo START: Starting database and generating demo data...
    docker-compose up -d postgres redis
    
    REM Wait for database to be ready
    echo WAIT: Waiting for database to be ready...
    timeout /t 10 /nobreak >nul
    
    REM Generate demo data
    echo DATA: Generating demo data (10,000 customers, 50,000 events)...
    docker-compose --profile setup run --rm data-generator
    
    if %errorlevel% neq 0 (
        echo ERROR: Failed to generate demo data
        pause
        exit /b 1
    )
    
    REM Mark as initialized
    echo. > .docker-initialized
    echo OK: Initial setup completed!
    echo.
)

echo START: Starting EngageHub CVM Platform...
echo.

REM Start all services
docker-compose up -d

if %errorlevel% neq 0 (
    echo ERROR: Failed to start services
    pause
    exit /b 1
)

echo WAIT: Waiting for services to start...
timeout /t 15 /nobreak >nul

REM Check service health
echo CHECK: Checking service health...
docker-compose ps

echo.
echo ========================================
echo    EngageHub CVM Platform is Ready!
echo ========================================
echo.
echo Frontend:     http://localhost:2020
echo Backend API:  http://localhost:3030
echo API Docs:     http://localhost:3030/docs
echo Database:     localhost:5432
echo Redis:        localhost:6379
echo.
echo Demo Login Credentials:
echo    Username: admin
echo    Password: admin
echo.
echo Tips:
echo    - Use 'docker-compose logs -f' to view logs
echo    - Use 'docker-compose down' to stop all services
echo    - Use 'docker-compose down -v' to reset all data
echo.

REM Open browser automatically
echo BROWSER: Opening EngageHub in your default browser...
start http://localhost:2020

echo.
echo SUCCESS: EngageHub CVM Platform is running successfully!
echo Press any key to view service logs, or close this window.
pause >nul

REM Show logs
docker-compose logs -f

REM Cleanup on exit
:cleanup
echo.
echo STOP: Stopping EngageHub services...
docker-compose down
echo OK: Services stopped. Goodbye!
pause