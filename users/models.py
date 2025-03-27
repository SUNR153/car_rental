from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICER = [
        ('renter', 'Арендатор'),
        ('owner', 'Арендодатель'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICER, default='renter')

    def __str__(self):
        return f"{self.username} ({self.role})"