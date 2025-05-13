import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from serviceprovider.models import Retailer
from customer.models import Customer
from .models import ChatMessage
from django.core.exceptions import ObjectDoesNotExist

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        room_name = text_data_json['room_name']

        # Save message to database
        try:
            await self.save_message(sender_id, room_name, message)
        except Exception as e:
            # Handle errors in saving message, like invalid user or room name format
            await self.send(text_data=json.dumps({'error': str(e)}))
            return

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'room_name': room_name
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'room_name': event['room_name']
        }))

    @database_sync_to_async
    def save_message(self, sender_id, room_name, message):
        try:
            # Extract user IDs from room name
            _, customer_id, retailer_id = room_name.split('_')
            
            sender = User.objects.get(id=sender_id)
            customer = Customer.objects.get(id=customer_id)
            retailer = Retailer.objects.get(id=retailer_id)

            # Ensure the sender is either the customer or retailer for the specific room
            if sender != customer.user and sender != retailer.user:
                raise PermissionError("Sender is not authorized to send messages in this room.")

            # Save the message
            ChatMessage.objects.create(
                sender=sender,
                retailer=retailer,
                customer=customer,
                message=message
            )
        except ObjectDoesNotExist as e:
            raise ValueError(f"One or more objects not found: {str(e)}")
        except Exception as e:
            raise Exception(f"Error saving message: {str(e)}")
