# 🚀 Manual Setup Guide (PowerShell)

Since the automated setup had issues, follow these manual steps:

## Step 1: Install Django and Dependencies

Run these commands one by one in PowerShell:

```powershell
# Install Django
pip install Django==4.2.9

# Install python-decouple (for .env)
pip install python-decouple==3.8

# Install Pillow (for images)
pip install Pillow==10.1.0

# Install openpyxl (for Excel)
pip install openpyxl==3.1.2

# Install pandas (for CSV/Excel parsing)
pip install pandas==2.1.4
```

**Note:** If pandas fails to install, you can skip it for now. The app will work with manual email entry and basic CSV parsing.

## Step 2: Run Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

## Step 3: Create Superuser (Admin Account)

```powershell
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

## Step 4: Start the Server

```powershell
python manage.py runserver
```

## Step 5: Access the Dashboard

Open your browser and go to:
- **Dashboard:** http://127.0.0.1:8000
- **Admin Panel:** http://127.0.0.1:8000/admin

## Alternative: Use PowerShell Script

Once packages are installed, you can use:

```powershell
.\start.ps1
```

## Troubleshooting

### "Django not installed" error
```powershell
pip install Django==4.2.9
```

### "decouple not installed" error  
```powershell
pip install python-decouple
```

### Pandas installation fails
Skip pandas for now. You can still:
- Enter emails manually
- Use basic CSV files
- Install pandas later when needed

### Port 8000 already in use
```powershell
python manage.py runserver 8080
```
Then visit http://127.0.0.1:8080

## Quick Commands Reference

```powershell
# Install all dependencies (one command)
pip install Django==4.2.9 python-decouple==3.8 Pillow==10.1.0 openpyxl==3.1.2

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver

# Or use the PowerShell script
.\start.ps1
```

## What You've Configured

✅ .env file is ready with SMTP settings
✅ All code files are created
✅ Templates are ready
✅ Static files are in place

You just need to:
1. Install Python packages
2. Run migrations
3. Create superuser
4. Start the server

## Next Steps After Setup

1. **Login** at http://127.0.0.1:8000/login
2. **Create a template** (optional)
3. **Send test email** using manual entry
4. **Check analytics** to see results

---

**Need help?** Check QUICKSTART.md or README.md for more details.
