
import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulk_email_dashboard.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_initial_admin():
    User = get_user_model()
    
    # Get credentials from environment or defaults
    username = os.environ.get('ADMIN_USERNAME', 'Yusuf')
    email = os.environ.get('ADMIN_EMAIL', 'yousufmoha255@gmail.com') # Using valid email
    password = os.environ.get('ADMIN_PASSWORD',     'Shiine1234')

    print(f"Checking for superuser: {username}")

    if not User.objects.filter(username=username).exists():
        print(f"User {username} not found. Creating superuser...")
        try:
            User.objects.create_superuser(username=username, email=email, password=password)
            print("Superuser created successfully!")
        except Exception as e:
            print(f"Error creating superuser: {e}")
    else:
        print(f"Superuser {username} already exists.")

if __name__ == "__main__":
    create_initial_admin()
