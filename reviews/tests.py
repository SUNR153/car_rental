from django.contrib.auth import get_user_model
from django.test import TestCase

from cars.models import Car
from .models import Review

User = get_user_model()


class ReviewModelTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='pass12345',
        )
        self.reviewer = User.objects.create_user(
            username='reviewer',
            email='reviewer@example.com',
            password='pass12345',
        )
        self.car = Car.objects.create(
            author=self.owner,
            brand='Toyota',
            model='Camry',
            year=2022,
            price_per_day='50.00',
        )

    def test_str_includes_author(self):
        review = Review.objects.create(
            car=self.car,
            author=self.reviewer,
            comment='Great car!',
        )
        self.assertEqual(str(review), f'Review by {self.reviewer}')

    def test_author_email_helper(self):
        review = Review.objects.create(
            car=self.car,
            author=self.reviewer,
            comment='Great car!',
        )
        self.assertEqual(review.author_email(), 'reviewer@example.com')

    def test_default_rating_is_five(self):
        review = Review.objects.create(
            car=self.car,
            author=self.reviewer,
            comment='Nice',
        )
        self.assertEqual(review.rating, 5)

    def test_review_can_exist_without_car(self):
        review = Review.objects.create(
            author=self.reviewer,
            comment='General feedback',
        )
        self.assertIsNone(review.car)
