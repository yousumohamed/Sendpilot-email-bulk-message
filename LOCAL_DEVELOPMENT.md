# Local Development Guide

## Django Bulk Email Sender - Localhost Only

This project is **configured for local development ONLY**. It is NOT intended for cloud deployment.

---

## Prerequisites

- Python 3.8+
- Gmail account with App Password enabled

---

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Gmail SMTP

1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Sign in with your Gmail account
3. Create a new App Password:
   - Select app: **Mail**
   - Select device: **Windows Computer** (or your OS)
4. Click **Generate**
5. **Copy the 16-character password** (e.g., `xxxx xxxx xxxx xxxx`)

### 3. Create `.env` File

Copy the example file:
```bash
copy .env.example .env
```

Edit `.env` and add your credentials:
```
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SENDER_EMAIL=your-email@gmail.com
SENDER_NAME=Your Name
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Visit: `http://localhost:8000`

---

## Email Configuration

### Current Settings (Local)

- **Email Backend:** Django SMTP
- **SMTP Host:** smtp.gmail.com
- **SMTP Port:** 587 (TLS)
- **Database:** SQLite (`db.sqlite3`)
- **Debug Mode:** Enabled

### Rate Limiting

Gmail free accounts have sending limits:
- **500 emails per day**
- **~1 email per second** recommended

The app includes a 1-second delay between emails by default.

---

## Troubleshooting

### Emails Not Sending

1. **Check App Password:**
   - You MUST use an App Password, not your regular Gmail password
   - Generate at: https://myaccount.google.com/apppasswords

2. **Check `.env` File:**
   - Ensure no spaces in the password
   - No quotes around values

3. **Check Gmail Security:**
   - 2-Factor Authentication must be enabled to create App Passwords

4. **Test SMTP Connection:**
   - Visit: `http://localhost:8000/debug-smtp/`
   - Click "Run SMTP Test"
   - Check error details

### Common Errors

| Error | Solution |
|-------|----------|
| `Authentication failed` | Wrong App Password - regenerate it |
| `Connection timeout` | Check your firewall/antivirus |
| `SMTP_USER not defined` | Add credentials to `.env` file |

---

## Project Structure

```
bulk_email_dashboard/
├── emails/              # Main app
│   ├── models.py       # Campaign, Email models
│   ├── views.py        # Dashboard, campaign views
│   ├── utils.py        # Email sending logic
│   └── templates/      # HTML templates
├── bulk_email_dashboard/
│   ├── settings.py     # Django settings (local only)
│   └── urls.py
├── db.sqlite3          # SQLite database (local)
├── .env                # Your secrets (DO NOT COMMIT)
├── .env.example        # Template for .env
└── requirements.txt    # Python dependencies
```

---

## Features

✅ Bulk email campaigns
✅ CSV/Excel recipient import
✅ Email personalization (merge tags)
✅ Campaign analytics
✅ Real-time sending status
✅ SMTP diagnostics page

---

## Security Notes

- **Never commit `.env` to Git**
- Use App Passwords, not your real Gmail password
- Keep `SECRET_KEY` private
- **This is for local use ONLY** - do not expose to the internet

---

## Need Help?

1. Check the SMTP Debug page: `/debug-smtp/`
2. Review Django logs in the terminal
3. Verify your Gmail App Password
