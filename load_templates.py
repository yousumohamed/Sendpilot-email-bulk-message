
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulk_email_dashboard.settings')
django.setup()

from django.contrib.auth.models import User
from emails.models import EmailTemplate

def create_templates():
    # specialized styles
    bg_color = "#F2EDD7"
    text_color = "#16194F"
    
    # Common Footer
    footer = f"""
    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid {text_color}; font-size: 12px; color: {text_color};">
        <p>
            <a href="https://somali-music.vercel.app/contact" style="color: {text_color}; text-decoration: none; font-weight: bold;">Contact Us</a> | 
            <a href="https://somali-music.vercel.app/download" style="color: {text_color}; text-decoration: none; font-weight: bold;">Download App</a> | 
            <a href="https://discord.com/invite/ryApNA5WDj" style="color: {text_color}; text-decoration: none; font-weight: bold;">Join Discord</a>
        </p>
        <p>© 2026 Somali Music. All rights reserved.</p>
        <p><a href="#" style="color: {text_color}; text-decoration: underline;">Unsubscribe</a></p>
    </div>
    """
    
    # Template 1: Welcome to Somali Music
    welcome_body = f"""
    <div style="background-color: {bg_color}; padding: 40px; font-family: Arial, sans-serif; color: {text_color};">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style="color: {text_color}; margin-bottom: 20px;">Welcome, {{name}}! 🎵</h1>
            
            <p style="font-size: 16px; line-height: 1.6;">
                Hi <strong style="color: {text_color};">{{name}}</strong>,
            </p>
            
            <p style="font-size: 16px; line-height: 1.6;">
                Thank you for joining <strong>Somali Music</strong>! We're excited to have you on board.
                Discover the best tracks, create playlists, and enjoy the rhythm of Somalia.
            </p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="https://somali-music.vercel.app/" style="background-color: {text_color}; color: {bg_color}; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">Start Listening</a>
            </div>
            
            {footer}
        </div>
    </div>
    """
    
    # Template 2: Download App
    app_body = f"""
    <div style="background-color: {bg_color}; padding: 40px; font-family: Arial, sans-serif; color: {text_color};">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style="color: {text_color}; margin-bottom: 20px;">Take Your Music Everywhere 📱</h1>
            
            <p style="font-size: 16px; line-height: 1.6;">
                Hello <strong style="color: {text_color};">{{name}}</strong>,
            </p>
            
            <p style="font-size: 16px; line-height: 1.6;">
                Did you know you can listen to your favorite Somali tracks offline? 
                Download our official mobile app today for the best experience!
            </p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="https://somali-music.vercel.app/download" style="background-color: {text_color}; color: {bg_color}; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">Download App</a>
            </div>
            
            {footer}
        </div>
    </div>
    """
    
    # Template 3: Discord Invite
    discord_body = f"""
    <div style="background-color: {bg_color}; padding: 40px; font-family: Arial, sans-serif; color: {text_color};">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style="color: {text_color}; margin-bottom: 20px;">Join Our Community! 💬</h1>
            
            <p style="font-size: 16px; line-height: 1.6;">
                Hey <strong style="color: {text_color};">{{name}}</strong>,
            </p>
            
            <p style="font-size: 16px; line-height: 1.6;">
                Want to discuss the latest hits, request songs, or just hang out with other music lovers?
                Join our official Discord server!
            </p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="https://discord.com/invite/ryApNA5WDj" style="background-color: #5865F2; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">Join Discord Server</a>
            </div>
            
            {footer}
        </div>
    </div>
    """
    
    # Get the first superuser or user to assign templates to
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.first()
        
    if not user:
        print("No user found! Please create a user first.")
        return

    # Create templates
    templates = [
        {
            "name": "Somali Music - Welcome",
            "subject": "Welcome to Somali Music, {name}!",
            "body": welcome_body
        },
        {
            "name": "Somali Music - Download App",
            "subject": "Download the Somali Music App 🎵",
            "body": app_body
        },
        {
            "name": "Somali Music - Discord Invite",
            "subject": "Join our Music Community! 🎧",
            "body": discord_body
        }
    ]

    for t in templates:
        EmailTemplate.objects.create(
            user=user,
            name=t["name"],
            subject=t["subject"],
            body=t["body"]
        )
        print(f"Created template: {t['name']}")

if __name__ == "__main__":
    create_templates()
