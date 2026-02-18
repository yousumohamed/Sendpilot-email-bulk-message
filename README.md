# Bulk Email Dashboard - LOCALHOST ONLY

A modern, feature-rich Django web application for sending bulk emails from your local machine. This project is configured strictly for local development and personal use using Gmail SMTP.

---

## 🚀 Quick Start (Local Only)

### 1. Setup Environment
```bash
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Configure Gmail SMTP
1. Enable 2FA on your Google Account.
2. Generate an **App Password** at [Google App Passwords](https://myaccount.google.com/apppasswords).
3. Create a `.env` file from `.env.example`:
   ```env
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-16-character-app-password
   SENDER_EMAIL=your-email@gmail.com
   ```

### 3. Initialize Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run Server
```bash
python manage.py runserver
```
Visit `http://localhost:8000`

---

## ✨ Features

### 🔐 User Authentication
- Secure login and signup system
- Only authenticated users can access the dashboard
- Session-based authentication

### 📊 Dashboard
- Real-time statistics overview:
  - Total emails sent
  - Delivered emails
  - Failed emails
  - Pending emails
- Interactive charts with Chart.js
- Recent campaigns overview
- Delivery rate visualization

### 📧 Email Sending
- **Multiple Input Methods:**
  - Upload Excel (.xlsx) or CSV files with email lists
  - Manual email entry (textarea)
- **Advanced Features:**
  - HTML email templates support
  - Personalization with placeholders ({name}, {email}, etc.)
  - File attachments (Excel, PDF, etc.)
  - Rate limiting (1-second delay between emails)
- **SMTP Support:**
  - Gmail (Strictly using App Passwords)
  - Localhost SMTP testing

### 📝 Email Templates
- Create reusable email templates
- Edit and delete templates
- Use placeholders for dynamic content
- Auto-fill subject and body when selected

### 📈 Analytics
- **Visual Analytics:**
  - Pie chart for email status breakdown
  - Bar chart for daily email activity (last 30 days)
  - Campaign performance metrics
- **Export Options:**
  - Download analytics as CSV
- **Detailed Metrics:**
  - Delivery rate per campaign
  - Success/failure ratios
  - Email status tracking

### 🎯 Campaign Management
- View all campaigns with status
- Detailed campaign view with:
  - Progress bars
  - Email list with individual statuses
  - Error messages for failed emails
- Campaign status tracking (Pending, In Progress, Completed, Failed)

### 🔒 Security & Best Practices
- Environment variables for sensitive data (.env)
- SMTP passwords never stored in code
- CSRF protection
- SQL injection prevention (Django ORM)
- Rate limiting to prevent email provider blocking
- Secure file upload handling

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd bulk_email_dashboard
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` and add your SMTP credentials:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# SMTP Configuration (Gmail Example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password-here
SENDER_EMAIL=your-email@gmail.com
SENDER_NAME=Bulk Email Dashboard
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## 📧 SMTP Configuration

### Gmail Setup (Recommended)
1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password
3. **Update .env:**
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SENDER_EMAIL=your-email@gmail.com
```

### Other Email Providers

**Outlook:**
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-password
```

**Yahoo:**
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
```

**SendGrid:**
```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key
```

## 📁 Email List Format

### CSV Format
```csv
email,name,company
john@example.com,John Doe,Acme Corp
jane@example.com,Jane Smith,Tech Inc
```

### Excel Format
Create an Excel file with columns:
- `email` (required)
- `name` (optional)
- `company` (optional)
- Any other custom fields

### Placeholders
Use placeholders in your email subject and body:
- `{email}` - Recipient's email
- `{name}` - Recipient's name
- `{company}` - Company name
- `{any_column}` - Any column from your file

**Example:**
```html
<h1>Hello {name}!</h1>
<p>Thank you for your interest, {name}.</p>
<p>We'll contact you at {email}.</p>
```

## 🎨 Tech Stack

- **Backend:** Django 4.2
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Charts:** Chart.js
- **Icons:** Bootstrap Icons
- **Database:** SQLite (local only)
- **Environment:** python-decouple (.env)
- **Email:** Django SMTP Backend

## 📂 Project Structure

```
bulk_email_dashboard/
├── bulk_email_dashboard/      # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── emails/                    # Main app
│   ├── migrations/
│   ├── templates/
│   │   └── emails/
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       ├── login.html
│   │       ├── signup.html
│   │       ├── send_email.html
│   │       ├── campaigns.html
│   │       ├── campaign_detail.html
│   │       ├── templates.html
│   │       ├── template_edit.html
│   │       ├── template_confirm_delete.html
│   │       └── analytics.html
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── utils.py
├── media/                     # Uploaded files
│   ├── uploads/
│   ├── attachments/
│   └── email_lists/
├── .env                       # Environment variables (not in git)
├── .env.example              # Example environment file
├── .gitignore
├── requirements.txt
├── manage.py
└── README.md
```

## 🔧 Admin Panel

Access the Django admin panel at `http://127.0.0.1:8000/admin/`

Features:
- View all users
- Manage campaigns
- View email statistics
- Monitor failed emails
- Access all email templates

## 🚨 Troubleshooting

### SMTP Authentication Failed
- **Gmail:** Make sure you're using an App Password, not your regular password
- **2FA:** Enable 2-Factor Authentication before generating App Password
- **Less Secure Apps:** Gmail no longer supports this; use App Passwords

### Emails Going to Spam
- Add SPF and DKIM records to your domain
- Warm up your email account (start with small batches)
- Avoid spam trigger words
- Include unsubscribe links

## 🚨 Local Sending Limits
- Gmail free accounts: **500 emails per day**.
- Recommended: **1 email per second** (the app handles this automatically).
- **DEBUG = True** is enabled for local troubleshooting.

### File Upload Issues
- Check file format (CSV or Excel)
- Ensure "email" column exists
- Verify file size (max 10MB recommended)

## 📝 Future Enhancements

- [ ] Email scheduling
- [ ] A/B testing
- [ ] Email open tracking
- [ ] Click tracking
- [ ] Unsubscribe management
- [ ] Email verification
- [ ] Advanced segmentation
- [ ] Multi-language support
- [ ] API integration
- [ ] Webhook support

## 📄 License

This project is dual-licensed under the [MIT License](LICENSE) and the [Apache License 2.0](LICENSE-APACHE).

## 🛡️ Security

For information on how to report a security vulnerability, please see our [Security Policy](SECURITY.md).

## 👨‍💻 Author


Created with ❤️ by <a href="https://yusuf-abdi.vercel.app/" target="_blank" rel="noopener noreferrer">Yusuf</a>
## 🤝 Contributing

Contributions, issues, and feature requests are welcome! See our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Note:** This application is for educational purposes. Always comply with email marketing laws (CAN-SPAM, GDPR, etc.) when sending bulk emails.
