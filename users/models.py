from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('renter', 'Renter'),  
        ('owner', 'Owner'),  
        ('moderator', 'Moderator'),  
        ('admin', 'Admin'),  
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='renter')
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ["email"]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, unique=True)
    driver_license = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.user.get_role_display()})" 
