@echo off
title EngageHub CVM Platform - Stop Services

echo.
echo ========================================
echo    Stopping EngageHub CVM Platform
echo ========================================
echo.

echo [STOP] Stopping all EngageHub services...
docker-compose down

if %errorlevel% neq 0 (
    echo [ERROR] Failed to stop services
    pause
    exit /b 1
)

echo [OK] All EngageHub services stopped successfully!
echo.
echo [TIP] To completely remove all data and start fresh:
echo    run: docker-compose down -v
echo.
pause