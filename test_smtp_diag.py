import os
import smtplib
from email.message import EmailMessage
from decouple import config

def test_smtp():
    # Load from .env
    host = config('SMTP_HOST', default='smtp.gmail.com')
    port = config('SMTP_PORT', default=587, cast=int)
    user = config('SMTP_USER', default='')
    password = config('SMTP_PASSWORD', default='')
    
    print(f"--- SMTP Diagnostic Test ---")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"User: {user}")
    print(f"Password: {'*' * len(password)}")
    print("-" * 30)

    msg = EmailMessage()
    msg.set_content("This is a test email from your local Bulk Email Dashboard.")
    msg['Subject'] = "SMTP Test Connection"
    msg['From'] = user
    msg['To'] = user

    try:
        print("Connecting to server...")
        server = smtplib.SMTP(host, port)
        server.set_debuglevel(1)
        
        print("Starting TLS...")
        server.starttls()
        
        print(f"Attempting login for {user}...")
        server.login(user, password)
        
        print("Login successful!")
        server.send_message(msg)
        print("Test email sent successfully!")
        
        server.quit()
        return True
    except smtplib.SMTPAuthenticationError:
        print("\n❌ ERROR: Authentication Failed (535)")
        print("This means Gmail rejected your credentials.")
        print("1. Ensure 'SMTP_USER' is your full email address.")
        print("2. Ensure 'SMTP_PASSWORD' is a 16-character APP PASSWORD, not your login password.")
        print("3. Check if 2-Factor Authentication is enabled on your Google Account.")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
    return False

if __name__ == "__main__":
    test_smtp()
