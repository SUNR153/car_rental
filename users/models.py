from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from datetime import timedelta
from django.utils import timezone


class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'), 
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    theme = models.CharField(max_length=20, default='light')
    language = models.CharField(max_length=10, default='en')
    background = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    driver_license = models.BooleanField(default=False)
    city = models.CharField(max_length=255, blank=True, null=True)
    MAP_CHOICES = [
    ('google', 'Google Maps'),
    ('yandex', 'Yandex Maps'),
    ('2gis', '2GIS'),
    ]

    preferred_map = models.CharField(max_length=20, choices=MAP_CHOICES, default='google')

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

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=1)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Reset code for {self.user.email}"