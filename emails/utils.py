import time
from django.utils import timezone
import pandas as pd
import re


def parse_email_file(file):
    """
    Parse CSV or Excel file to extract email addresses and additional data
    Returns: list of dictionaries with email and other fields
    """
    try:
        file_extension = file.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            df = pd.read_csv(file)
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format. Please use CSV or Excel files.")
        
        # Convert DataFrame to list of dictionaries
        email_data = []
        
        # Try to find email column (case-insensitive)
        email_column = None
        for col in df.columns:
            if col.lower() in ['email', 'email address', 'e-mail', 'mail']:
                email_column = col
                break
        
        if not email_column:
            # If no email column found, assume first column contains emails
            email_column = df.columns[0]
        
        for _, row in df.iterrows():
            email = str(row[email_column]).strip()
            
            # Validate email format
            if is_valid_email(email):
                data = {'email': email}
                
                # Add other columns as personalization data
                for col in df.columns:
                    if col != email_column:
                        # Convert column name to placeholder format
                        placeholder = col.lower().replace(' ', '_')
                        data[placeholder] = str(row[col]) if pd.notna(row[col]) else ''
                
                email_data.append(data)
        
        return email_data
    
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to parse email file: {str(e)}", exc_info=True)
        raise Exception(f"Error parsing file: {str(e)}")


def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def parse_manual_emails(email_text):
    """
    Parse manually entered emails (one per line)
    Returns: list of dictionaries with email
    """
    emails = []
    lines = email_text.strip().split('\n')
    
    for line in lines:
        email = line.strip()
        if email and is_valid_email(email):
            emails.append({'email': email})
    
    return emails


def personalize_content(content, data):
    """
    Replace placeholders in content with actual data
    Example: "Hello {name}" with data={'name': 'John'} becomes "Hello John"
    """
    for key, value in data.items():
        placeholder = '{' + key + '}'
        content = content.replace(placeholder, str(value))
    
    return content



def send_email(recipient_email, subject, body, attachments=None, personalization_data=None):
    """
    Send email using Django's EmailMultiAlternatives (Production Safe)
    Returns: (success: bool, error_message: str or None)
    """
    try:
        from django.core.mail import EmailMultiAlternatives
        from django.utils.html import strip_tags
        from django.conf import settings

        # Personalize content if data provided
        if personalization_data:
            subject = personalize_content(subject, personalization_data)
            body = personalize_content(body, personalization_data)

        text_body = strip_tags(body)
        
        # Create Email Message
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
            reply_to=[settings.DEFAULT_FROM_EMAIL]
        )
        msg.attach_alternative(body, "text/html")

        # Handle Attachments
        if attachments:
            for attachment in attachments:
                try:
                    # Check if attachment is an UploadedFile or file path
                    if hasattr(attachment, 'read'):
                        attachment.seek(0)
                        content = attachment.read()
                        name = attachment.name
                        attachment.seek(0) # Reset pointer
                    else:
                        continue # Skip unknown types

                    msg.attach(name, content)
                except Exception as e:
                    print(f"Error attaching file: {e}")

        # Send
        msg.send(fail_silently=False)
        return True, None

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"SMTP Email Error sending to {recipient_email}: {e}", exc_info=True)
        return False, str(e)


def send_bulk_emails(campaign, email_list, attachments=None, delay=1):
    """
    Send emails to multiple recipients with rate limiting
    
    Args:
        campaign: EmailCampaign instance
        email_list: List of dictionaries with 'email' and optional personalization data
        attachments: List of file objects
        delay: Delay in seconds between emails (for rate limiting)
    
    Returns: (sent_count, failed_count)
    """
    from .models import Email
    
    sent_count = 0
    failed_count = 0
    
    campaign.status = 'in_progress'
    campaign.total_emails = len(email_list)
    campaign.save()
    
    for email_data in email_list:
        recipient_email = email_data.get('email')
        recipient_name = email_data.get('name', email_data.get('first_name', ''))
        
        # Remove 'email' from personalization data
        personalization_data = {k: v for k, v in email_data.items() if k != 'email'}
        
        # Create Email record
        email_record = Email.objects.create(
            campaign=campaign,
            recipient_email=recipient_email,
            recipient_name=recipient_name,
            subject=campaign.subject,
            body=campaign.body,
            personalization_data=personalization_data,
            status='pending'
        )
        
        # Send email
        success, error_message = send_email(
            recipient_email=recipient_email,
            subject=campaign.subject,
            body=campaign.body,
            attachments=attachments,
            personalization_data=personalization_data
        )
        
        # Update email record
        if success:
            email_record.status = 'delivered'
            email_record.sent_at = timezone.now()
            sent_count += 1
        else:
            email_record.status = 'failed'
            email_record.error_message = error_message
            failed_count += 1
        
        email_record.save()
        
        # Update campaign progress
        campaign.sent_emails = sent_count + failed_count
        campaign.failed_emails = failed_count
        campaign.save()
        
        # Rate limiting - delay between emails
        if delay > 0:
            time.sleep(delay)
    
    # Mark campaign as completed
    campaign.status = 'completed'
    campaign.completed_at = timezone.now()
    campaign.save()
    
    return sent_count, failed_count
