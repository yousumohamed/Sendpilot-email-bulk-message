
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config

def test_smtp_connection():
    try:
        # Load configuration
        smtp_host = config('SMTP_HOST', default='smtp.gmail.com')
        smtp_port = config('SMTP_PORT', default=587, cast=int)
        smtp_user = config('SMTP_USER', default='')
        smtp_password = config('SMTP_PASSWORD', default='')
        sender_email = config('SENDER_EMAIL', default=smtp_user)

        print(f"DEBUG: SMTP_HOST={smtp_host}")
        print(f"DEBUG: SMTP_PORT={smtp_port}")
        print(f"DEBUG: SMTP_USER={smtp_user}")
        print(f"DEBUG: SENDER_EMAIL={sender_email}")
        print(f"DEBUG: Password is {'set' if smtp_password else 'NOT SET'}")

        if not smtp_user or not smtp_password:
            print("ERROR: SMTP_USER or SMTP_PASSWORD is not set in .env file.")
            return

        # Prepare test email
        recipient_email = smtp_user  # Send to self for testing
        subject = "Test Email from Debug Script"
        body = "This is a test email sent from the debug script to verify SMTP settings."

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        print("\nAttempting to connect to SMTP server...")
        
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.set_debuglevel(1)  # Enable debug output
        
        print("Connected. Starting TLS...")
        server.ehlo()
        server.starttls()
        server.ehlo()
        
        print("Logging in...")
        server.login(smtp_user, smtp_password)
        print("Logged in successfully.")
        
        print(f"Sending email to {recipient_email}...")
        server.send_message(msg)
        print("Email sent successfully!")
        
        server.quit()
        print("\nSUCCESS: The email was accepted by the SMTP server.")
        print("Please check your INBOX and SPAM folder for the test email.")
        print("If you don't see it, it might be blocked by Google or your provider.")

    except Exception as e:
        print(f"\nERROR: Failed to send email. Exception: {e}")

if __name__ == "__main__":
    test_smtp_connection()
