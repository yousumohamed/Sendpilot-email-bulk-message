import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from .models import EmailCampaign


class CampaignProgressConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer that streams live progress updates for a single campaign.

    Clients connect to: ws://<host>/ws/campaign-progress/<campaign_id>/
    """

    async def connect(self):
        user = self.scope.get("user", AnonymousUser())
        campaign_id = self.scope["url_route"]["kwargs"].get("campaign_id")

        # Basic auth/ownership check – only allow owner of campaign
        if not user.is_authenticated:
            await self.close()
            return

        try:
            campaign = await self._get_campaign(campaign_id)
        except EmailCampaign.DoesNotExist:
            await self.close()
            return

        if campaign.user_id != user.id:
            await self.close()
            return

        self.campaign_id = campaign_id
        self.group_name = f"campaign_{campaign_id}_{user.id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def campaign_progress(self, event):
        """
        Handler for messages sent to the group with type 'campaign.progress'.
        """
        payload = event.get("payload", {})
        # Add a server-side timestamp if not present
        payload.setdefault("server_time", timezone.now().isoformat())
        await self.send(text_data=json.dumps(payload))

    @staticmethod
    async def _get_campaign(campaign_id):
        # Small async wrapper for ORM access
        return await EmailCampaign.objects.aget(pk=campaign_id)

