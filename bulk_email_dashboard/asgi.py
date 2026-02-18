"""
ASGI config for bulk_email_dashboard project.

It exposes the ASGI callable as a module-level variable named ``application``.

This configuration supports both traditional HTTP and WebSocket connections
using Django Channels.
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulk_email_dashboard.settings')

django_asgi_app = get_asgi_application()

import emails.routing  # noqa: E402

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            emails.routing.websocket_urlpatterns
        )
    ),
})
