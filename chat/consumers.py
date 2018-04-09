import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import Message


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

        # Save message to database
        message = await self.save_message(message_sender, message_text)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_text': message_text,
                'message_sender': message_sender,
                'message_send_datetime': message.get_create_datetime()
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

    @database_sync_to_async
    def save_message(self, message_sender_username: str, message_text: str) -> Message:
        user_model = get_user_model()
        user = user_model.objects.get(username=message_sender_username)
        return Message.objects.create(author=user, text=message_text, chat_id=self.room_name)
