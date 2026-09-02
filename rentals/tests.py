from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from cars.models import Car
from .models import Rental

User = get_user_model()


class RentalModelTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='pass12345',
        )
        self.customer = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='pass12345',
        )
        self.car = Car.objects.create(
            author=self.owner,
            brand='Toyota',
            model='Camry',
            year=2022,
            price_per_day='50.00',
        )

    def test_total_price_auto_calculated_when_not_provided(self):
        rental = Rental(
            car=self.car,
            customer=self.customer,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 5),
        )
        rental.save()

        # 5 inclusive days * 50.00/day
        self.assertEqual(rental.total_price, Decimal('250.00'))

    def test_total_price_single_day(self):
        rental = Rental(
            car=self.car,
            customer=self.customer,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 1),
        )
        rental.save()

        self.assertEqual(rental.total_price, Decimal('50.00'))

    def test_explicit_total_price_is_not_overridden(self):
        rental = Rental(
            car=self.car,
            customer=self.customer,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 5),
            total_price=Decimal('999.00'),
        )
        rental.save()

        self.assertEqual(rental.total_price, Decimal('999.00'))
