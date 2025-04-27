# chats/models.py
from django.db import models
from django.contrib.auth import get_user_model
from cars.models import Car

User = get_user_model()

class Chat(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='chats')
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat for {self.car.brand} {self.car.model}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.email} → {self.chat.car.brand} {self.chat.car.model}: {self.content[:20]}"
