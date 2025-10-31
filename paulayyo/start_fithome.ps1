# FitHome Pro - PowerShell Launcher
# Fitness Portal Launcher for Windows

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    FitHome Pro - Fitness Portal" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import streamlit, pandas, matplotlib, plotly, seaborn, numpy" 2>$null
    Write-Host "✅ All dependencies are installed" -ForegroundColor Green
} catch {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error: Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Check if database exists
if (-not (Test-Path "fithome_pro.db")) {
    Write-Host "Creating database..." -ForegroundColor Yellow
    python init_database.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error: Failed to create database" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "✅ Database created successfully" -ForegroundColor Green
}

# Get local IP for mobile access
try {
    $localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.254.*"} | Select-Object -First 1).IPAddress
} catch {
    $localIP = "localhost"
}

# Show access information
Write-Host ""
Write-Host "🚀 Starting FitHome Pro server..." -ForegroundColor Green
Write-Host ""
Write-Host "📱 ACCESS METHODS:" -ForegroundColor Cyan
Write-Host "   • Desktop: http://localhost:8501" -ForegroundColor White
Write-Host "   • Mobile:  http://$localIP`:8501" -ForegroundColor White
Write-Host ""
Write-Host "👤 DEMO ACCOUNT:" -ForegroundColor Cyan
Write-Host "   • Email: demo@fithome.com" -ForegroundColor White
Write-Host "   • Password: hello" -ForegroundColor White
Write-Host ""
Write-Host "🔄 Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the application
try {
    python -m streamlit run main.py --server.port 8501 --server.address 0.0.0.0
} catch {
    Write-Host "❌ Error starting server" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Read-Host "Press Enter to exit"
