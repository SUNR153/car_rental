from django.db import models
from cars.models import Car
from users.models import User
from django.core.validators import MinValueValidator
from datetime import timedelta

class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    def save(self, *args, **kwargs):
        if not self.total_price and self.start_date and self.end_date:
            days = (self.end_date - self.start_date).days + 1
            self.total_price = days * self.car.price_per_day
        super().save(*args, **kwargs)
