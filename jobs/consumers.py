# jobs/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class JobAlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Group name for all candidates
        await self.channel_layer.group_add("job_alerts", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("job_alerts", self.channel_name)

    async def job_alert(self, event):
        # Send job alert to WebSocket
        await self.send(text_data=json.dumps({
            "title": event["title"],
            "company": event["company"],
            "location": event["location"],
        }))
