import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message_text']
        message_sender = text_data_json['message_sender']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_text': message_text,
                'message_sender': message_sender,
                'message_send_datetime': timezone.now().strftime('%d.%m.%Y %H:%M:%S')
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message_text = event['message_text']
        message_sender = event['message_sender']
        message_send_datetime = event['message_send_datetime']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message_text': message_text,
            'message_sender': message_sender,
            'message_send_datetime': message_send_datetime
        }))
