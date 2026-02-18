
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from decouple import config

def test_html_email():
    try:
        # Load configuration
        smtp_host = config('SMTP_HOST', default='smtp.gmail.com')
        smtp_port = config('SMTP_PORT', default=587, cast=int)
        smtp_user = config('SMTP_USER', default='')
        smtp_password = config('SMTP_PASSWORD', default='')
        sender_email = config('SENDER_EMAIL', default=smtp_user)
        sender_name = "Debug Script"

        print(f"DEBUG: Testing HTML email sending...")
        
        # Prepare test email similar to the app but simplified
        recipient_email = smtp_user  # Send to self for testing
        subject = "Test HTML Email 🚀"
        
        # Create message container
        msg = MIMEMultipart('alternative')
        
        # Use simple header setting first to test
        msg['From'] = formataddr((str(Header(sender_name, 'utf-8')), sender_email))
        msg['To'] = recipient_email
        msg['Subject'] = Header(subject, 'utf-8')
        
        # Note: intentionally NOT setting Date or Message-ID manually to let library handle it
        
        # Content
        text_body = "This is a plain text version of the HTML email."
        html_body = """
        <html>
          <body>
            <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f0f0f0;">
                <div style="background-color: white; padding: 20px; border-radius: 8px;">
                    <h1 style="color: #4a4a4a;">HTML Email Test 🧪</h1>
                    <p>This is a <strong>formatted</strong> email sent from the debug script.</p>
                    <p>If you see this, HTML sending works!</p>
                    <a href="https://example.com" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Click Me</a>
                </div>
            </div>
          </body>
        </html>
        """
        
        part1 = MIMEText(text_body, 'plain', 'utf-8')
        part2 = MIMEText(html_body, 'html', 'utf-8')
        
        msg.attach(part1)
        msg.attach(part2)

        # Connect to SMTP server
        print("Connecting to SMTP...")
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.ehlo()
        
        print(f"Logging in as {smtp_user}...")
        server.login(smtp_user, smtp_password)
        
        print(f"Sending HTML email to {recipient_email}...")
        server.send_message(msg)
        print("Email sent successfully!")
        
        server.quit()
        print("\nSUCCESS: HTML Email accepted by server.")
        print("Please check your INBOX (and SPAM) for 'Test HTML Email 🚀'.")

    except Exception as e:
        print(f"\nERROR: Failed to send email. Exception: {e}")

if __name__ == "__main__":
    test_html_email()
