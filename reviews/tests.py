from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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


class ReviewViewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='pass12345',
        )
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
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
        self.review = Review.objects.create(
            car=self.car,
            author=self.author,
            comment='Great car!',
        )

    def test_review_update_forbidden_for_non_author(self):
        self.client.login(username='stranger@example.com', password='pass12345')
        response = self.client.get(reverse('reviews:review_update', args=[self.review.pk]))
        self.assertEqual(response.status_code, 403)

    def test_review_update_allowed_for_author(self):
        self.client.login(username='author@example.com', password='pass12345')
        response = self.client.get(reverse('reviews:review_update', args=[self.review.pk]))
        self.assertEqual(response.status_code, 200)

    def test_review_delete_forbidden_for_non_author(self):
        self.client.login(username='stranger@example.com', password='pass12345')
        response = self.client.post(reverse('reviews:review_delete', args=[self.review.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Review.objects.filter(pk=self.review.pk).exists())
