from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from users.models import User
from django.conf import settings

class Car(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    CATEGORY_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('hatchback', 'Hatchback'),
        ('coupe', 'Coupe'),
        ('other', 'Other'),
    ]
    
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    
    FUEL_TYPE_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
        ('semi-automatic', 'Semi-Automatic'),
    ]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1980),
            MaxValueValidator(datetime.now().year + 1)
        ]
    )
    price_per_day = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    location = models.CharField(max_length=100, default='', blank=True)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default='good'
    )
    mileage = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_TYPE_CHOICES,
        default='petrol'
    )
    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_CHOICES,
        default='automatic'
    )
    seats = models.PositiveSmallIntegerField(
        default=4,
        validators=[
            MinValueValidator(2),
            MaxValueValidator(8)
        ]
    )
    features = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

    class Meta:
        ordering = ['-year', 'brand']

    def author_email(self):
        return self.author.email
    author_email.short_description = 'Email автора'

    def __str__(self):
        return f"Review by {self.author}"