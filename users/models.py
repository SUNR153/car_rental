from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
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

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, unique=True)
    driver_license = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    theme = models.CharField(max_length=20, default='light')
    language = models.CharField(max_length=10, default='en')

    def __str__(self):
        return f"{self.user.username} ({self.user.get_role_display()})"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            phone=instance.phone or f"default-{instance.pk}"
        )
