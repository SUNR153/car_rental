from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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


class FavoriteViewTests(TestCase):
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

    def test_add_to_favorites_requires_login(self):
        response = self.client.get(reverse('favorites:add_to_favorites', args=[self.car.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Favorite.objects.exists())

    def test_add_to_favorites_creates_entry(self):
        self.client.login(username='fan@example.com', password='pass12345')
        self.client.get(reverse('favorites:add_to_favorites', args=[self.car.pk]))
        self.assertTrue(Favorite.objects.filter(user=self.user, car=self.car).exists())

    def test_add_to_favorites_is_idempotent(self):
        self.client.login(username='fan@example.com', password='pass12345')
        self.client.get(reverse('favorites:add_to_favorites', args=[self.car.pk]))
        self.client.get(reverse('favorites:add_to_favorites', args=[self.car.pk]))
        self.assertEqual(Favorite.objects.filter(user=self.user, car=self.car).count(), 1)

    def test_remove_from_favorites(self):
        Favorite.objects.create(user=self.user, car=self.car)
        self.client.login(username='fan@example.com', password='pass12345')
        self.client.get(reverse('favorites:remove_from_favorites', args=[self.car.pk]))
        self.assertFalse(Favorite.objects.filter(user=self.user, car=self.car).exists())

    def test_favorites_list_only_shows_own_favorites(self):
        other_user = User.objects.create_user(
            username='other', email='other@example.com', password='pass12345',
        )
        Favorite.objects.create(user=self.user, car=self.car)
        Favorite.objects.create(user=other_user, car=self.car)

        self.client.login(username='fan@example.com', password='pass12345')
        response = self.client.get(reverse('favorites:favorites_list'))
        self.assertEqual(len(response.context['favorites']), 1)
