# # chats/consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from .models import Chat, Message
# from notifications.models import Notification  # Добавляем Notification
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.chat_id = self.scope['url_route']['kwargs']['chat_id']
#         self.chat_group_name = f'chat_{self.chat_id}'

#         if await self.has_access():
#             await self.channel_layer.group_add(
#                 self.chat_group_name,
#                 self.channel_name
#             )
#             await self.accept()
#         else:
#             await self.close()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.chat entendimento, self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         content = text_data_json['content']
#         user = self.scope['user']

#         # Сохраняем сообщение и отправляем уведомление
#         message = await self.create_message(content, user)

#         # Отправляем сообщение всем участникам группы
#         await self.channel_layer.group_send(
#             self.chat_group_name,
#             {
#                 'type': 'chat_message',
#                 'content': content,
#                 'sender': user.email,
#                 'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
#             }
#         )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             'content': event['content'],
#             'sender': event['sender'],
#             'created_at': event['created_at'],
#         }))

#     @database_sync_to_async
#     def has_access(self):
#         chat = Chat.objects.get(id=self.chat_id)
#         return self.scope['user'].is_authenticated and self.scope['user'] in chat.participants.all()

#     @database_sync_to_async
#     def create_message(self, content, user):
#         chat = Chat.objects.get(id=self.chat_id)
#         message = Message.objects.create(chat=chat, sender=user, content=content)
        
#         # Отправляем уведомление собеседнику
#         for participant in chat.participants.all():
#             if participant != user:  # Уведомляем только другого участника
#                 Notification.objects.create(
#                     user=participant,
#                     message=f"Новое сообщение от {user.email} в чате по автомобилю {chat.car.name}"
#                 )
#         return message