# Quick Start Guide - Bulk Email Dashboard

## 🚀 Getting Started in 5 Minutes


### Step 2: Configure SMTP Settings
1. Open `.env` file in a text editor
2. Add your email credentials:

**For Gmail:**
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SENDER_EMAIL=your-email@gmail.com
SENDER_NAME=Your Name
```

**How to get Gmail App Password:**
1. Go to https://myaccount.google.com/apppasswords
2. Enable 2-Factor Authentication if not already enabled
3. Select "Mail" and your device
4. Copy the 16-character password (no spaces)

### Step 3: Start the Server
Double-click `run.bat` or run in terminal:
```bash
run.bat
```

### Step 4: Access the Dashboard
Open your browser and go to:
- **Dashboard:** http://127.0.0.1:8000
- **Admin Panel:** http://127.0.0.1:8000/admin

### Step 5: Send Your First Email

1. **Sign Up / Login**
   - Create a new account or login with your credentials

2. **Create a Template (Optional)**
   - Go to "Templates" in the sidebar
   - Create a reusable email template
   - Use placeholders like `{name}`, `{company}`, etc.

3. **Send Bulk Email**
   - Click "Send Emails" in the sidebar
   - Fill in campaign details:
     - Campaign Name: "Welcome Campaign"
     - Subject: "Welcome {name}!"
     - Body: HTML content with placeholders
   
   - **Choose Recipients:**
     - **Option A:** Upload `sample_email_list.csv` (included)
     - **Option B:** Type emails manually (one per line)
   
   - Click "Send Campaign"

4. **Monitor Progress**
   - Go to "Campaigns" to see status
   - Click "View" to see detailed results
   - Check "Analytics" for charts and statistics

## 📧 Sample Email Template

**Subject:**
```
Welcome to our service, {name}!
```

**Body:**
```html
<h1>Hello {name}!</h1>
<p>Thank you for joining us at <strong>{company}</strong>.</p>
<p>We're excited to have you as our {position}!</p>
<p>We'll keep you updated at {email}.</p>
<br>
<p>Best regards,<br>The Team</p>
```

## 🎯 Features Overview

### Dashboard
- View total emails, delivered, failed, and pending
- See delivery rate percentage
- View recent campaigns
- Interactive charts

### Send Emails
- Upload CSV/Excel files
- Manual email entry
- HTML email support
- File attachments
- Personalization with placeholders

### Templates
- Create reusable templates
- Edit and delete templates
- Use in campaigns

### Campaigns
- View all campaigns
- Track status (Pending, In Progress, Completed, Failed)
- See detailed email list with individual statuses

### Analytics
- Email status breakdown (pie chart)
- Daily activity (bar chart)
- Campaign performance table
- Download data as CSV

## 🔧 Troubleshooting

### "Django not installed" error
Run `setup.bat` again to reinstall dependencies.

### SMTP Authentication Failed
- Make sure you're using an **App Password**, not your regular Gmail password
- Enable 2-Factor Authentication on your Google account first
- Check that SMTP credentials in `.env` are correct

### Emails not sending
- Check your `.env` file has correct SMTP settings
- Verify your internet connection
- Check Gmail's daily sending limit (500 emails/day for free accounts)

### Port already in use
If port 8000 is busy, run:
```bash
python manage.py runserver 8080
```
Then visit http://127.0.0.1:8080

## 📝 Manual Setup (Alternative)

If `setup.bat` doesn't work, run these commands manually:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env with your SMTP credentials

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## 🎨 Next Steps

1. **Customize Templates:** Create professional email templates
2. **Test with Sample Data:** Use `sample_email_list.csv`
3. **Monitor Analytics:** Check delivery rates and optimize
4. **Scale Up:** Integrate with SendGrid or other services for higher volumes

## 📞 Support

For issues or questions:
- Check the main `README.md` for detailed documentation
- Review the troubleshooting section
- Check Django logs for error messages

## ⚠️ Important Notes

- **Gmail Limits:** Free Gmail accounts can send ~500 emails/day
- **Rate Limiting:** Emails are sent with 1-second delay to avoid blocking
- **Compliance:** Always follow email marketing laws (CAN-SPAM, GDPR)
- **Testing:** Test with a small list first before sending to large audiences

---

**Enjoy sending bulk emails! 🚀**
