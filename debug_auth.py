
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulk_email_dashboard.settings')
django.setup()

from django.contrib.auth import get_user_model

print(f"Using Database: {settings.DATABASES['default']['NAME']}")

User = get_user_model()
username = 'Yusuf'

try:
    user = User.objects.get(username=username)
    print(f"User: {user.username}")
    print(f"  is_active: {user.is_active}")
    print(f"  is_staff: {user.is_staff}")
    print(f"  is_superuser: {user.is_superuser}")
    
    if not user.is_staff:
        print("!! WARNING: User is not staff. Fixing...")
        user.is_staff = True
        user.save()
        print("  -> Fixed is_staff")

    if not user.is_superuser:
        print("!! WARNING: User is not superuser. Fixing...")
        user.is_superuser = True
        user.save()
        print("  -> Fixed is_superuser")

except User.DoesNotExist:
    print(f"User {username} not found")
