from django.db import models
from cars.models import Car
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

class Review(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    car = models.ForeignKey(  # Добавьте это, если отзыв привязан к машине
        Car,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def author_email(self):
        return self.author.email
    author_email.short_description = 'Email автора'

    def __str__(self):
        return f"Review by {self.author}"
