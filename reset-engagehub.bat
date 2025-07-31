@echo off
title EngageHub CVM Platform - Reset Data

echo.
echo ========================================
echo    Reset EngageHub CVM Platform
echo ========================================
echo.

echo [WARNING] This will delete ALL data and reset the platform!
echo.
set /p confirm="Are you sure you want to continue? (y/N): "

if /i not "%confirm%"=="y" (
    echo [CANCEL] Reset cancelled.
    pause
    exit /b 0
)

echo.
echo [STOP] Stopping all services...
docker-compose down

echo [CLEAN] Removing all data volumes...
docker-compose down -v

echo [PRUNE] Cleaning up Docker images...
docker system prune -f

echo [RESET] Removing initialization marker...
if exist ".docker-initialized" del ".docker-initialized"

echo.
echo [OK] EngageHub has been completely reset!
echo.
echo [INFO] To start fresh, run: launch-engagehub.bat
echo.
pause