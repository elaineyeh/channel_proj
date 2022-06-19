from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.name = self.scope['url_route']['kwargs']['name']

        await self.channel_layer.group_add(
            'lobby',
            self.channel_name
        )

        await self.accept()
        await self.group_send(f'{self.name} join the room.')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'lobby',
            self.channel_name
        )

        await self.group_send(f'{self.name} left the room.')

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = self.name + ': ' + text_data_json['message']

        await self.group_send(message)

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def group_send(self, msg, group='lobby', type_='chat_message'):
        await self.channel_layer.group_send(
            group,
            {
                'type': type_,
                'message': msg
            }
        )