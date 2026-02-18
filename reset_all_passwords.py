
import os
import django
from django.db.utils import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulk_email_dashboard.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
password = 'Shiine1234'

def reset_user(username):
    try:
        user = User.objects.get(username=username)
        print(f"Updating existing user: {username}")
    except User.DoesNotExist:
        print(f"Creating new superuser: {username}")
        user = User(username=username)

    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.is_active = True
    try:
        user.save()
        print(f"-> Success! Username: '{username}' | Password: '{password}'")
    except Exception as e:
        print(f"-> Error saving user {username}: {e}")

# Reset main targets
usernames = ['Yusuf', 'admin', 'Jose']

print("Resetting/Creating Superusers...")
for u in usernames:
    reset_user(u)

print("\nVerify Users in Database:")
for user in User.objects.all():
    print(f"User: {user.username} (Staff: {user.is_staff})")
