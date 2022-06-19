from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.name = self.scope['url_route']['kwargs']['name']

        async_to_sync(self.channel_layer.group_add)(
            'lobby',
            self.channel_name
        )

        self.accept()
        self.group_send(f'{self.name} join the room.')

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'lobby',
            self.channel_name
        )

        self.group_send(f'{self.name} left the room.')

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = self.name + ': ' + text_data_json['message']

        self.group_send(message)

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

    def group_send(self, msg, group='lobby', type_='chat_message'):
        async_to_sync(self.channel_layer.group_send)(
            group,
            {
                'type': type_,
                'message': msg
            }
        )