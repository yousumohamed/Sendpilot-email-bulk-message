# Quick Start Script for PowerShell
Write-Host "Starting Bulk Email Dashboard..." -ForegroundColor Cyan
Write-Host ""

# Run migrations
Write-Host "Running migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

# Start server
Write-Host ""
Write-Host "Starting Django development server..." -ForegroundColor Green
Write-Host "Dashboard: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Admin Panel: http://127.0.0.1:8000/admin" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver
