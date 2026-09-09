import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            self.group_name = f"user_{self.scope['user'].id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # 🔔 Handle new notification
    async def notify(self, event):
        await self.send(text_data=json.dumps({
            "type": "notify",   # matches base.html JS
            "id": event.get("id"),
            "message": event["message"],
            "url": event.get("url", "#")
        }))

    # 🔔 Handle single notification marked as read
    async def read(self, event):
        await self.send(text_data=json.dumps({
            "type": "read",     # matches base.html JS
            "id": event["id"]
        }))

    # 🔔 Handle all notifications marked as read
    async def read_all(self, event):
        await self.send(text_data=json.dumps({
            "type": "read_all"  # matches base.html JS
        }))
