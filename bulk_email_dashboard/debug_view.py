
from django.conf import settings
from django.http import HttpResponse

def debug_auth_view(request):
    try:
        if not request.user.is_authenticated:
            return HttpResponse("User is NOT logged in. <a href='/admin/login/?next=/debug-auth/'>Login</a>")
        
        lines = []
        lines.append(f"DB Name: {settings.DATABASES['default']['NAME']}")
        lines.append(f"Authenticated: {request.user.is_authenticated}")
        lines.append(f"Username: {request.user.username}")
        lines.append(f"Is Active: {request.user.is_active}")
        lines.append(f"Is Staff: {request.user.is_staff}")
        lines.append(f"Is Superuser: {request.user.is_superuser}")
        
        # Check password valid? No, can't check easily without knowing plain password, oh wait I set it to Shiine1234
        lines.append(f"Password Check (Shiine1234): {request.user.check_password('Shiine1234')}")
        
        return HttpResponse("<br>".join(lines))
        
    except Exception as e:
        return HttpResponse(f"Error: {e}")
