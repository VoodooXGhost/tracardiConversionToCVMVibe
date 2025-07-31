@echo off
title EngageHub - Docker Test

echo.
echo ========================================
echo    EngageHub Docker Environment Test
echo ========================================
echo.

echo [TEST] Checking Docker installation...
docker --version
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed or not in PATH
    echo Please install Docker Desktop for Windows
    pause
    exit /b 1
)

echo [TEST] Checking Docker service status...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker service is not running
    echo Please start Docker Desktop and try again
    pause
    exit /b 1
)

echo [TEST] Checking Docker Compose...
docker-compose --version
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose is not available
    pause
    exit /b 1
)

echo [TEST] Testing Docker functionality...
docker run --rm hello-world >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker cannot run containers
    echo Please check Docker Desktop settings
    pause
    exit /b 1
)

echo.
echo [SUCCESS] All Docker tests passed!
echo [INFO] Your system is ready to run EngageHub
echo.
echo [NEXT] Run launch-engagehub.bat to start the platform
echo.
pause