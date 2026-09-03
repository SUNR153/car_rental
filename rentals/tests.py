from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cars.models import Car, CarAvailability
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


class RentalViewTests(TestCase):
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
        self.stranger = User.objects.create_user(
            username='stranger',
            email='stranger@example.com',
            password='pass12345',
        )
        self.car = Car.objects.create(
            author=self.owner,
            brand='Toyota',
            model='Camry',
            year=2022,
            price_per_day='50.00',
        )
        CarAvailability.objects.create(
            car=self.car,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
        )
        self.rental = Rental.objects.create(
            car=self.car,
            customer=self.customer,
            start_date=date(2026, 2, 1),
            end_date=date(2026, 2, 5),
        )

    def test_rental_create_requires_login(self):
        response = self.client.get(reverse('rentals:rental_create', args=[self.car.pk]))
        self.assertEqual(response.status_code, 302)

    def test_rental_create_within_availability_window(self):
        self.client.login(username='customer@example.com', password='pass12345')
        response = self.client.post(
            reverse('rentals:rental_create', args=[self.car.pk]),
            {'start_date': '2026-03-01', 'end_date': '2026-03-03'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Rental.objects.filter(car=self.car, start_date=date(2026, 3, 1)).exists()
        )

    def test_rental_create_outside_availability_window_is_rejected(self):
        self.client.login(username='customer@example.com', password='pass12345')
        response = self.client.post(
            reverse('rentals:rental_create', args=[self.car.pk]),
            {'start_date': '2027-03-01', 'end_date': '2027-03-03'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Rental.objects.filter(start_date=date(2027, 3, 1)).exists()
        )

    def test_rental_update_forbidden_for_stranger(self):
        self.client.login(username='stranger@example.com', password='pass12345')
        response = self.client.get(reverse('rentals:rental_update', args=[self.rental.pk]))
        self.assertEqual(response.status_code, 403)

    def test_rental_update_allowed_for_customer(self):
        self.client.login(username='customer@example.com', password='pass12345')
        response = self.client.get(reverse('rentals:rental_update', args=[self.rental.pk]))
        self.assertEqual(response.status_code, 200)

    def test_rental_delete_forbidden_for_stranger(self):
        self.client.login(username='stranger@example.com', password='pass12345')
        response = self.client.post(reverse('rentals:rental_delete', args=[self.rental.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Rental.objects.filter(pk=self.rental.pk).exists())

    def test_rental_delete_allowed_for_owner(self):
        self.client.login(username='owner@example.com', password='pass12345')
        response = self.client.post(reverse('rentals:rental_delete', args=[self.rental.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Rental.objects.filter(pk=self.rental.pk).exists())

    def test_rental_extend_forbidden_for_non_customer(self):
        self.client.login(username='stranger@example.com', password='pass12345')
        response = self.client.post(
            reverse('rentals:rental_extend', args=[self.rental.pk]),
            {'start_date': '2026-02-01', 'end_date': '2026-02-06'},
        )
        self.assertEqual(response.status_code, 403)
