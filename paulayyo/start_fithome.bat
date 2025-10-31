@echo off
title FitHome Pro Launcher
echo.
echo ========================================
echo    FitHome Pro - Fitness Portal
echo ========================================
echo.
echo Starting FitHome Pro...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if database exists
if not exist "fithome_pro.db" (
    echo Creating database...
    python init_database.py
    if errorlevel 1 (
        echo Error: Failed to create database
        pause
        exit /b 1
    )
)

REM Start the application
echo.
echo Starting FitHome Pro server...
echo.
echo Access URLs:
echo   Desktop: http://localhost:8501
echo   Mobile:  http://[your-ip]:8501
echo.
echo Demo Account:
echo   Email: demo@fithome.com
echo   Password: hello
echo.
echo Press Ctrl+C to stop the server
echo.

REM Find Chrome path
set CHROME_PATH=
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
) else if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe
)

REM Start Streamlit and wait a bit for server to be ready
echo.
echo Opening browser in 8 seconds...
start /min python -m streamlit run main.py --server.port 8501 --server.address 0.0.0.0
timeout /t 8 /nobreak >nul

REM Open Chrome
echo Opening Chrome...
if defined CHROME_PATH (
    start "" "%CHROME_PATH%" http://localhost:8501
) else (
    echo Chrome not found, opening with default browser...
    start http://localhost:8501
)

echo.
echo FitHome Pro is running!
echo Press any key to close this window (server will keep running)
pause
