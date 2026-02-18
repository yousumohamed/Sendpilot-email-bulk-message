@echo off
echo Starting Bulk Email Dashboard...
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure your SMTP settings.
    pause
)

REM Run the development server
echo Starting Django development server...
echo.
echo Dashboard: http://127.0.0.1:8000
echo Admin Panel: http://127.0.0.1:8000/admin
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver
