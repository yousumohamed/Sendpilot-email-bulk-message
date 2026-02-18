from django.contrib import admin
from .models import EmailTemplate, EmailCampaign, Email, EmailAttachment, EmailList


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'subject', 'created_at', 'updated_at']
    list_filter = ['created_at', 'user']
    search_fields = ['name', 'subject', 'body']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'status', 'total_emails', 'sent_emails', 
                    'failed_emails', 'created_at', 'completed_at']
    list_filter = ['status', 'created_at', 'user']
    search_fields = ['name', 'subject']
    readonly_fields = ['created_at', 'completed_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['recipient_email', 'recipient_name', 'campaign', 'status', 
                    'sent_at', 'created_at']
    list_filter = ['status', 'created_at', 'campaign']
    search_fields = ['recipient_email', 'recipient_name', 'subject']
    readonly_fields = ['created_at', 'sent_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(campaign__user=request.user)


@admin.register(EmailAttachment)
class EmailAttachmentAdmin(admin.ModelAdmin):
    list_display = ['filename', 'campaign', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['filename']
    readonly_fields = ['uploaded_at']


@admin.register(EmailList)
class EmailListAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'total_emails', 'uploaded_at']
    list_filter = ['uploaded_at', 'user']
    search_fields = ['name']
    readonly_fields = ['uploaded_at', 'total_emails']
