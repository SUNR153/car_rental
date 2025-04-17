from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    #password = models.CharField(max_length=128)
    ROLE_CHOICES = [
        ('renter', 'Renter'),  
        ('owner', 'Owner'),  
        ('moderator', 'Moderator'),  
        ('admin', 'Admin'),  
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='renter')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, unique=True)
    driver_license = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.user.get_role_display()})"