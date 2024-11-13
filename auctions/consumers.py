# auctions/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BidConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.item_id = self.scope['url_route']['kwargs']['item_id']
        self.room_group_name = f'auction_{self.item_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        amount = data['amount']
        # Aqui você pode adicionar lógica para verificar e atualizar o lance no banco de dados
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'bid_update',
                'amount': amount
            }
        )

    async def bid_update(self, event):
        amount = event['amount']
        await self.send(text_data=json.dumps({
            'amount': amount
        }))
