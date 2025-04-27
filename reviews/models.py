from django.db import models
from cars.models import Car
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)  # Связь с автомобилем, обязательно
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def author_email(self):
        return self.author.email
    author_email.short_description = 'Email автора'

    def __str__(self):
        return f"Review by {self.author}"
