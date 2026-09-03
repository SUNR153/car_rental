from django.contrib.auth import get_user_model
from django.test import TestCase

from cars.models import Car
from .models import Favorite

User = get_user_model()


class FavoriteModelTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='pass12345',
        )
        self.user = User.objects.create_user(
            username='fan',
            email='fan@example.com',
            password='pass12345',
        )
        self.car = Car.objects.create(
            author=self.owner,
            brand='Toyota',
            model='Camry',
            year=2022,
            price_per_day='50.00',
        )

    def test_str_includes_user_and_car(self):
        favorite = Favorite.objects.create(user=self.user, car=self.car)
        self.assertEqual(str(favorite), 'fan@example.com -> Toyota Camry')

    def test_related_names(self):
        Favorite.objects.create(user=self.user, car=self.car)
        self.assertEqual(self.user.favorites.count(), 1)
        self.assertEqual(self.car.favorited_by.count(), 1)
