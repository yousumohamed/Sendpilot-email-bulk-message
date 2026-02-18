
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulk_email_dashboard.settings')
django.setup()

from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

credentials = [
    ('Yusuf', 'Shiine1234'),
    ('admin', 'Shiine1234'),
    ('admin2', 'Shiine1234'),
]

print(f"Checking authentication against DB: {settings.DATABASES['default']['NAME']}")

for username, password in credentials:
    user = authenticate(username=username, password=password)
    if user is not None:
        print(f"SUCCESS: User '{username}' authenticated successfully.")
        print(f"  Active: {user.is_active}, Staff: {user.is_staff}, Superuser: {user.is_superuser}")
    else:
        print(f"FAILURE: User '{username}' failed to authenticate.")
        try:
            u = User.objects.get(username=username)
            print(f"  (User exists in DB. Password match confirm: {u.check_password(password)})")
        except User.DoesNotExist:
            print("  (User does not exist in DB)")
