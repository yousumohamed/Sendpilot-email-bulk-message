from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r"^ws/campaign-progress/(?P<campaign_id>\d+)/$",
        consumers.CampaignProgressConsumer.as_asgi(),
        name="ws_campaign_progress",
    ),
]

