import json
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import Room, Message
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):
      def connect(self):
            self.accept()

      def receive(self,text_data):
            print(text_data)
            text_json = json.loads(text_data)
            message = text_json['message']
            print(message)
            self.send( text_data=json.dumps({'message':message}) )
            
      def disconnect(self, message):
            pass

class ChatConsumere(WebsocketConsumer):
      def connect(self):
            self.room_name = self.scope['url_route']['kwargs']['room']
            self.room_group_name = 'chat_%s' % self.room_name
            # print(self.room_group_name)

             # Join room group
            async_to_sync(self.channel_layer.group_add)(
                  self.room_group_name,
                  self.channel_name
            )

            self.accept()

      def receive(self,text_data):
            text_data_json = json.loads(text_data)
            # print(text_data)
            message = text_data_json['message']
           
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                  self.room_group_name,
                  {
                        'type': 'chat_message',
                        'message': message
                  }
            )

      def chat_message(self,event):
            # print(event)
            message = event['message']
            # # Send message to WebSocket
            self.send(text_data=json.dumps({
                  'message': message
            }))      
            
      def disconnect(self, close_code):
            # Leave room group
            async_to_sync(self.channel_layer.group_discard)(
                  self.room_group_name,
                  self.channel_name
            )

class ChatConsumerA(AsyncWebsocketConsumer):
      async def connect(self):
            # print(self.scope['url_route']['kwargs'])
            self.user = self.scope['user']
            self.room_name = self.scope['url_route']['kwargs']['room']
            self.room_group_name = 'chat_%s' % self.room_name
            # print(self.room_group_name)           
             # Join room group
            await self.channel_layer.group_add(
                  self.room_group_name,
                  self.channel_name
            )

            await self.accept()

      async def receive(self,text_data):
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            sender = text_data_json['sender']
            print(self)
            # call fx to save message to db
            await self.create_message(message,sender)
            
            # Send message to room group  
            await self.channel_layer.group_send(
                  self.room_group_name,
                  {
                        'type': 'chat_message',
                        'message': message,
                        'sender':sender
                  }
            )
    
      async def chat_message(self,event):
            # print(event)
            message = event['message']
            sender = event['sender']
            # # Send message to WebSocket
            await self.send(text_data=json.dumps({
                  'message': message,
                  'sender':sender
            }))      
            
      async def disconnect(self, close_code):
            # Leave room group
            await self.channel_layer.group_discard(
                  self.room_group_name,
                  self.channel_name
            )

      @database_sync_to_async
      def create_message(self,message,sender):
            room = Room.objects.get(name=self.room_name)
            sender = User.objects.get(username=sender)
            return Message.objects.create(room=room, sender=sender, message=message)
