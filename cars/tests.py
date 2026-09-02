from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Car, CarAvailability

User = get_user_model()


class CarModelTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='pass12345',
        )

    def make_car(self, **overrides):
        defaults = dict(
            author=self.author,
            brand='Toyota',
            model='Camry',
            year=2022,
            price_per_day='50.00',
        )
        defaults.update(overrides)
        return Car.objects.create(**defaults)

    def test_str_returns_brand_model_year(self):
        car = self.make_car()
        self.assertEqual(str(car), 'Toyota Camry (2022)')

    def test_author_email_helper(self):
        car = self.make_car()
        self.assertEqual(car.author_email(), 'owner@example.com')

    def test_default_values(self):
        car = self.make_car()
        self.assertTrue(car.is_available)
        self.assertEqual(car.category, 'other')
        self.assertEqual(car.condition, 'good')
        self.assertEqual(car.fuel_type, 'petrol')
        self.assertEqual(car.transmission, 'automatic')
        self.assertEqual(car.seats, 4)

    def test_negative_price_is_invalid(self):
        car = self.make_car(price_per_day='-10.00')
        with self.assertRaises(ValidationError):
            car.full_clean()

    def test_seats_out_of_range_is_invalid(self):
        car = self.make_car(seats=1)
        with self.assertRaises(ValidationError):
            car.full_clean()

    def test_ordering_is_by_year_desc_then_brand(self):
        older = self.make_car(brand='Honda', model='Civic', year=2018)
        newer = self.make_car(brand='BMW', model='X5', year=2023)
        same_year_a = self.make_car(brand='Audi', model='A4', year=2020)
        same_year_b = self.make_car(brand='Kia', model='Rio', year=2020)

        cars = list(Car.objects.all())
        self.assertEqual(cars[0], newer)
        self.assertEqual(cars[-1], older)
        self.assertLess(
            cars.index(same_year_a),
            cars.index(same_year_b),
        )


class CarAvailabilityModelTests(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(
            username='owner2',
            email='owner2@example.com',
            password='pass12345',
        )
        self.car = Car.objects.create(
            author=self.author,
            brand='Kia',
            model='Sportage',
            year=2021,
            price_per_day='40.00',
        )

    def test_str_includes_car_and_dates(self):
        availability = CarAvailability.objects.create(
            car=self.car,
            start_date='2026-01-01',
            end_date='2026-01-10',
        )
        self.assertIn(str(self.car), str(availability))
        self.assertIn('2026-01-01', str(availability))
