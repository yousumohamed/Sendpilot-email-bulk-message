@echo off
echo ========================================
echo Bulk Email Dashboard Setup Script
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Step 4: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo Step 5: Creating .env file...
if not exist .env (
    copy .env.example .env
    echo .env file created! Please edit it with your SMTP credentials.
) else (
    echo .env file already exists.
)
echo.

echo Step 6: Running migrations...
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)
echo Migrations completed successfully!
echo.

echo Step 7: Creating superuser...
echo Please create an admin account:
python manage.py createsuperuser
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the development server, run:
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Then visit: http://127.0.0.1:8000
echo Admin panel: http://127.0.0.1:8000/admin
echo.
pause
