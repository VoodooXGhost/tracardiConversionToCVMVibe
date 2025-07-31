@echo off
echo Starting EngageHub...

docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not running!
    pause
    exit /b 1
)

echo Docker is running
echo Building and starting services...

docker-compose up -d --build

echo.
echo EngageHub is starting at http://localhost:2020
echo Press any key to open browser...
pause >nul

start http://localhost:2020

echo.
echo Press any key to stop services...
pause >nul

docker-compose down