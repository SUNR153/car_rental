from django.db import models
from cars.models import Car
from users.models import User

class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.author.username} на {self.car} — {self.rating}★"
