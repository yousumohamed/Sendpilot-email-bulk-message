from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.dashboard_view, name='dashboard'),
    
    # Templates
    path('templates/', views.templates_view, name='templates'),
    path('templates/<int:pk>/edit/', views.template_edit_view, name='template_edit'),
    path('templates/<int:pk>/delete/', views.template_delete_view, name='template_delete'),
    path('templates/<int:pk>/ajax/', views.get_template_ajax, name='template_ajax'),
    
    # Email Sending
    path('send/', views.send_email_view, name='send_email'),
    
    # Campaigns
    path('campaigns/', views.campaigns_view, name='campaigns'),
    path('campaigns/<int:pk>/', views.campaign_detail_view, name='campaign_detail'),
    
    # Analytics
    path('analytics/', views.analytics_view, name='analytics'),
    path('analytics/download/', views.download_analytics_csv, name='download_analytics'),
    
    # SMTP Debug
    path('debug-smtp/', views.debug_smtp_view, name='debug_smtp'),
]
