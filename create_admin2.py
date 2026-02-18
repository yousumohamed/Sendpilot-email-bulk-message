
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulk_email_dashboard.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'admin2'
password = 'Shiine1234'

try:
    user = User.objects.create_superuser(username=username, email='', password=password)
    print(f"Created new superuser: '{username}' with password '{password}'")
except Exception as e:
    print(f"Error creating user {username}: {e}")
