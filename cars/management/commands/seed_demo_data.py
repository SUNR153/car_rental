import random
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from cars.models import Car, CarAvailability
from favorite.models import Favorite
from notifications.models import Notification
from reviews.models import Review

User = get_user_model()

CARS = [
    dict(brand='Toyota', model='Camry', year=2022, price_per_day=45, category='sedan',
         condition='excellent', fuel_type='petrol', transmission='automatic', seats=5,
         mileage=18000, location='Almaty'),
    dict(brand='Toyota', model='RAV4', year=2023, price_per_day=60, category='suv',
         condition='excellent', fuel_type='hybrid', transmission='automatic', seats=5,
         mileage=8000, location='Almaty'),
    dict(brand='Hyundai', model='Elantra', year=2021, price_per_day=35, category='sedan',
         condition='good', fuel_type='petrol', transmission='automatic', seats=5,
         mileage=32000, location='Astana'),
    dict(brand='Kia', model='Sportage', year=2022, price_per_day=50, category='suv',
         condition='good', fuel_type='petrol', transmission='automatic', seats=5,
         mileage=21000, location='Astana'),
    dict(brand='Volkswagen', model='Polo', year=2020, price_per_day=28, category='hatchback',
         condition='good', fuel_type='petrol', transmission='manual', seats=5,
         mileage=45000, location='Shymkent'),
    dict(brand='BMW', model='3 Series', year=2023, price_per_day=90, category='sedan',
         condition='excellent', fuel_type='petrol', transmission='automatic', seats=5,
         mileage=5000, location='Almaty'),
    dict(brand='BMW', model='X5', year=2021, price_per_day=110, category='suv',
         condition='good', fuel_type='diesel', transmission='automatic', seats=7,
         mileage=39000, location='Almaty'),
    dict(brand='Chevrolet', model='Cobalt', year=2019, price_per_day=22, category='sedan',
         condition='fair', fuel_type='petrol', transmission='manual', seats=5,
         mileage=68000, location='Shymkent'),
    dict(brand='Tesla', model='Model 3', year=2023, price_per_day=95, category='sedan',
         condition='excellent', fuel_type='electric', transmission='automatic', seats=5,
         mileage=3000, location='Astana'),
    dict(brand='Mini', model='Cooper', year=2020, price_per_day=40, category='coupe',
         condition='good', fuel_type='petrol', transmission='manual', seats=4,
         mileage=27000, location='Almaty'),
]

REVIEW_COMMENTS = [
    'Great car, very clean and well maintained.',
    'Smooth ride, would rent again.',
    'Owner was responsive and pickup was easy.',
    'Good value for the price.',
    'A bit older than expected but ran fine.',
]


class Command(BaseCommand):
    help = 'Seeds the database with demo cars, users, reviews and notifications.'

    def handle(self, *args, **options):
        owner, created = User.objects.get_or_create(
            email='demo.owner@vrooom.example',
            defaults=dict(username='demo_owner', first_name='Demo', last_name='Owner'),
        )
        if created:
            owner.set_password('demopass123')
            owner.save()

        customers = []
        for i in range(1, 4):
            customer, created = User.objects.get_or_create(
                email=f'demo.customer{i}@vrooom.example',
                defaults=dict(username=f'demo_customer{i}', first_name=f'Customer{i}'),
            )
            if created:
                customer.set_password('demopass123')
                customer.profile.driver_license = True
                customer.profile.save()
                customer.save()
            customers.append(customer)

        created_cars = []
        for data in CARS:
            car, created = Car.objects.get_or_create(
                brand=data['brand'],
                model=data['model'],
                year=data['year'],
                defaults=dict(author=owner, **{k: v for k, v in data.items() if k not in ('brand', 'model', 'year')}),
            )
            created_cars.append(car)

            if created:
                CarAvailability.objects.create(
                    car=car,
                    start_date=date.today(),
                    end_date=date.today() + timedelta(days=90),
                )

        for car in created_cars:
            if not Review.objects.filter(car=car).exists():
                for customer in random.sample(customers, k=random.randint(1, len(customers))):
                    Review.objects.create(
                        car=car,
                        author=customer,
                        comment=random.choice(REVIEW_COMMENTS),
                        rating=random.randint(3, 5),
                    )

            if not Favorite.objects.filter(car=car).exists() and random.random() > 0.5:
                Favorite.objects.get_or_create(user=random.choice(customers), car=car)

        for customer in customers:
            Notification.objects.get_or_create(
                user=customer,
                message='Welcome to VROOOM! Browse cars and book your first ride.',
            )

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {len(created_cars)} cars, {len(customers)} customers, and 1 owner.'
        ))
        self.stdout.write('Demo login: demo.customer1@vrooom.example / demopass123')
