
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulk_email_dashboard.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'Yusuf'
password = 'Shiine1234'

try:
    user = User.objects.get(username=username)
    print(f"User '{username}' found.")
    print(f"Current status - Active: {user.is_active}, Staff: {user.is_staff}, Superuser: {user.is_superuser}")
    
    # Force permissions
    user.is_active = True
    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save()
    
    print(f"Updated status - Active: {user.is_active}, Staff: {user.is_staff}, Superuser: {user.is_superuser}")
    print(f"Password reset to: {password}")

except User.DoesNotExist:
    print(f"User '{username}' not found. Creating it...")
    User.objects.create_superuser(username=username, password=password, email='')
    print(f"User '{username}' created with password '{password}'")

print("\n--- All Users ---")
for u in User.objects.all():
    print(f"User: {u.username} | Staff: {u.is_staff} | Superuser: {u.is_superuser} | Active: {u.is_active}")
