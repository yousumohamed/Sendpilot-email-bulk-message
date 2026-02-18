from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncDate
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import timedelta
import csv
import threading
import time

from .models import EmailTemplate, EmailCampaign, Email, EmailAttachment, EmailList
from .forms import SignUpForm, LoginForm, EmailTemplateForm, EmailCampaignForm
from .utils import parse_email_file, parse_manual_emails, send_bulk_emails

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def signup_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'emails/signup.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'emails/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


def _broadcast_campaign_progress(campaign_id: int, user_id: int, total_emails: int):
    """
    Poll campaign/email state and push progress updates over WebSocket.

    This does NOT modify the core email-sending logic; it simply observes
    database state and emits events while a campaign is running.
    """
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    group_name = f"campaign_{campaign_id}_{user_id}"

    while True:
        try:
            campaign = EmailCampaign.objects.get(pk=campaign_id)
        except EmailCampaign.DoesNotExist:
            break

        sent = campaign.sent_emails
        failed = campaign.failed_emails
        pending = max(campaign.pending_emails, 0)
        total = total_emails or campaign.total_emails or (sent + failed + pending)

        payload = {
            "campaign_id": campaign_id,
            "status": campaign.status,
            "sent": sent,
            "failed": failed,
            "pending": pending,
            "total": total,
        }

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "campaign.progress",
                "payload": payload,
            },
        )

        if campaign.status in ("completed", "failed") or (total and sent + failed >= total):
            break

        time.sleep(1.0)


@login_required
def dashboard_view(request):
    """Main dashboard view with statistics"""
    # Get user's campaigns
    campaigns = EmailCampaign.objects.filter(user=request.user)
    
    # Calculate statistics
    total_emails = Email.objects.filter(campaign__user=request.user).count()
    delivered_emails = Email.objects.filter(
        campaign__user=request.user,
        status='delivered'
    ).count()
    failed_emails = Email.objects.filter(
        campaign__user=request.user,
        status='failed'
    ).count()
    pending_emails = Email.objects.filter(
        campaign__user=request.user,
        status='pending'
    ).count()
    
    # Recent campaigns
    recent_campaigns = campaigns.order_by('-created_at')[:5]
    
    # Get emails per day for the last 7 days
    seven_days_ago = timezone.now() - timedelta(days=7)
    emails_per_day = Email.objects.filter(
        campaign__user=request.user,
        created_at__gte=seven_days_ago
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    # Calculate delivery rate
    delivery_rate = 0
    if total_emails > 0:
        delivery_rate = round((delivered_emails / total_emails) * 100, 2)
    
    context = {
        'total_emails': total_emails,
        'delivered_emails': delivered_emails,
        'failed_emails': failed_emails,
        'pending_emails': pending_emails,
        'delivery_rate': delivery_rate,
        'recent_campaigns': recent_campaigns,
        'emails_per_day': list(emails_per_day),
    }
    
    return render(request, 'emails/dashboard.html', context)


@login_required
def templates_view(request):
    """Email templates management view"""
    templates = EmailTemplate.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.user = request.user
            template.save()
            messages.success(request, 'Template created successfully!')
            return redirect('templates')
    else:
        form = EmailTemplateForm()
    
    context = {
        'templates': templates,
        'form': form,
    }
    
    return render(request, 'emails/templates.html', context)


@login_required
def template_edit_view(request, pk):
    """Edit email template"""
    template = get_object_or_404(EmailTemplate, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            messages.success(request, 'Template updated successfully!')
            return redirect('templates')
    else:
        form = EmailTemplateForm(instance=template)
    
    context = {
        'form': form,
        'template': template,
    }
    
    return render(request, 'emails/template_edit.html', context)


@login_required
def template_delete_view(request, pk):
    """Delete email template"""
    template = get_object_or_404(EmailTemplate, pk=pk, user=request.user)
    
    if request.method == 'POST':
        template.delete()
        messages.success(request, 'Template deleted successfully!')
        return redirect('templates')
    
    return render(request, 'emails/template_confirm_delete.html', {'template': template})


@login_required
def send_email_view(request):
    """Send bulk email view"""
    if request.method == 'POST':
        form = EmailCampaignForm(request.POST, request.FILES, user=request.user)
        
        if form.is_valid():
            try:
                # Create campaign
                campaign = form.save(commit=False)
                campaign.user = request.user
                campaign.save()
                
                # Parse email list
                email_list = []
                
                # Check for uploaded file
                if 'email_list_file' in request.FILES:
                    file = request.FILES['email_list_file']
                    email_list = parse_email_file(file)
                    
                    # Save email list record
                    EmailList.objects.create(
                        user=request.user,
                        name=file.name,
                        file=file,
                        total_emails=len(email_list)
                    )
                
                # Check for manual emails
                elif form.cleaned_data.get('manual_emails'):
                    email_list = parse_manual_emails(form.cleaned_data['manual_emails'])
                
                if not email_list:
                    messages.error(request, 'Please provide email addresses either by uploading a file or entering them manually.')
                    return redirect('send_email')
                
                # Handle attachments
                attachments = []
                if 'attachments' in request.FILES:
                    for file in request.FILES.getlist('attachments'):
                        attachment = EmailAttachment.objects.create(
                            campaign=campaign,
                            file=file,
                            filename=file.name
                        )
                        attachments.append(attachment.file)
                
                # Send emails in background thread
                def send_emails_background():
                    send_bulk_emails(
                        campaign=campaign,
                        email_list=email_list,
                        attachments=attachments,
                        delay=1  # 1 second delay between emails
                    )
                
                thread = threading.Thread(target=send_emails_background)
                thread.daemon = True
                thread.start()

                # Start a separate background thread to broadcast live progress
                progress_thread = threading.Thread(
                    target=_broadcast_campaign_progress,
                    args=(campaign.id, request.user.id, len(email_list)),
                )
                progress_thread.daemon = True
                progress_thread.start()

                messages.success(request, f'Campaign "{campaign.name}" created! Sending {len(email_list)} emails in the background.')
                return redirect('campaigns')
            
            except Exception as e:
                messages.error(request, f'Error creating campaign: {str(e)}')
    else:
        form = EmailCampaignForm(user=request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'emails/send_email.html', context)


@login_required
def campaigns_view(request):
    """View all campaigns"""
    campaigns = EmailCampaign.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'campaigns': campaigns,
    }
    
    return render(request, 'emails/campaigns.html', context)


@login_required
def campaign_detail_view(request, pk):
    """View campaign details"""
    campaign = get_object_or_404(EmailCampaign, pk=pk, user=request.user)
    emails = Email.objects.filter(campaign=campaign).order_by('-created_at')
    
    context = {
        'campaign': campaign,
        'emails': emails,
    }
    
    return render(request, 'emails/campaign_detail.html', context)


@login_required
def analytics_view(request):
    """Analytics view with charts and statistics"""
    # Get all emails for the user
    emails = Email.objects.filter(campaign__user=request.user)
    
    # Status breakdown
    status_breakdown = emails.values('status').annotate(count=Count('id'))
    
    # Emails per day for the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    emails_per_day = emails.filter(
        created_at__gte=thirty_days_ago
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        total=Count('id'),
        delivered=Count('id', filter=Q(status='delivered')),
        failed=Count('id', filter=Q(status='failed'))
    ).order_by('date')
    
    # Campaign statistics
    campaign_stats = EmailCampaign.objects.filter(user=request.user).values(
        'name', 'total_emails', 'sent_emails', 'failed_emails', 'status'
    ).order_by('-created_at')[:10]
    
    context = {
        'status_breakdown': list(status_breakdown),
        'emails_per_day': list(emails_per_day),
        'campaign_stats': list(campaign_stats),
    }
    
    return render(request, 'emails/analytics.html', context)


@login_required
def download_analytics_csv(request):
    """Download analytics data as CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="email_analytics.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Campaign', 'Recipient Email', 'Recipient Name', 'Status', 
                     'Sent At', 'Error Message'])
    
    emails = Email.objects.filter(campaign__user=request.user).select_related('campaign')
    
    for email in emails:
        writer.writerow([
            email.campaign.name,
            email.recipient_email,
            email.recipient_name,
            email.status,
            email.sent_at.strftime('%Y-%m-%d %H:%M:%S') if email.sent_at else '',
            email.error_message
        ])
    
    return response


@login_required
def get_template_ajax(request, pk):
    """AJAX endpoint to get template data"""
    template = get_object_or_404(EmailTemplate, pk=pk, user=request.user)
    
    data = {
        'subject': template.subject,
        'body': template.body,
    }
    

from decouple import config

@login_required
def debug_smtp_view(request):
    """View to debug SMTP settings and send a test email"""
    smtp_host = config('SMTP_HOST', default='smtp.gmail.com')
    smtp_port = config('SMTP_PORT', default=587)
    smtp_user = config('SMTP_USER', default='')
    smtp_password = config('SMTP_PASSWORD', default='')
    
    success = False
    test_attempted = False
    error_log = ""
    
    if request.method == "POST":
        test_attempted = True
        try:
            from .utils import send_email
            
            # Use current user's email if available, else fallback to SMTP User (usually admin)
            recipient = request.user.email if request.user.email else smtp_user
            
            if not recipient:
                raise ValueError("No recipient email found. Please ensure your user profile has an email or SMTP_USER is set.")
            
            success, error_log = send_email(
                recipient_email=recipient,
                subject="SMTP Test Email 🚀",
                body=f"This is a test email sent by {request.user.username} from the diagnostics page.<br>If you see this, your configuration works!"
            )
            
            if success:
                 messages.success(request, f"Test email sent to {recipient}!")
            else:
                 messages.error(request, f"Failed to send email: {error_log}")
                 
        except Exception as e:
            success = False
            error_log = str(e)
            messages.error(request, f"Error: {e}")

    context = {
        'smtp_host': smtp_host,
        'smtp_port': smtp_port,
        'smtp_user': smtp_user,
        'smtp_password_set': bool(smtp_password),
        'success': success,
        'test_attempted': test_attempted,
        'error_log': error_log
    }
    
    return render(request, 'emails/debug_smtp.html', context)
