from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import PasswordResetCode, Profile

User = get_user_model()


class UserModelTests(TestCase):
    def test_email_is_username_field(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_str_includes_email_and_role(self):
        user = User.objects.create_user(
            username='john',
            email='john@example.com',
            password='pass12345',
        )
        self.assertEqual(str(user), 'john@example.com (User)')

    def test_default_role_is_user(self):
        user = User.objects.create_user(
            username='jane',
            email='jane@example.com',
            password='pass12345',
        )
        self.assertEqual(user.role, 'user')


class ProfileSignalTests(TestCase):
    def test_profile_created_automatically_on_user_creation(self):
        user = User.objects.create_user(
            username='alice',
            email='alice@example.com',
            password='pass12345',
            phone='+1234567890',
        )
        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertEqual(user.profile.phone, '+1234567890')

    def test_profile_gets_default_phone_when_user_has_none(self):
        user = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='pass12345',
        )
        self.assertEqual(user.profile.phone, f'default-{user.pk}')


class PasswordResetCodeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='reset_user',
            email='reset@example.com',
            password='pass12345',
        )

    def test_expires_at_defaults_to_one_hour_from_creation(self):
        code = PasswordResetCode.objects.create(user=self.user)
        expected = timezone.now() + timedelta(hours=1)
        delta = abs((code.expires_at - expected).total_seconds())
        self.assertLess(delta, 5)

    def test_is_expired_false_for_fresh_code(self):
        code = PasswordResetCode.objects.create(user=self.user)
        self.assertFalse(code.is_expired())

    def test_is_expired_true_for_past_code(self):
        code = PasswordResetCode.objects.create(
            user=self.user,
            expires_at=timezone.now() - timedelta(minutes=1),
        )
        self.assertTrue(code.is_expired())


class UserViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='pass12345',
        )
        self.other_user = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='pass12345',
        )

    def test_login_view_get_returns_200(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_with_correct_credentials_redirects(self):
        response = self.client.post(reverse('users:login'), {
            'email': 'owner@example.com',
            'password': 'pass12345',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_with_wrong_password_stays_on_page(self):
        response = self.client.post(reverse('users:login'), {
            'email': 'owner@example.com',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)

    def test_profile_requires_login(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)

    def test_user_update_requires_login(self):
        response = self.client.get(reverse('users:user_update', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)

    def test_user_update_forbidden_for_other_user(self):
        self.client.login(username='other@example.com', password='pass12345')
        response = self.client.get(reverse('users:user_update', args=[self.user.pk]))
        self.assertEqual(response.status_code, 403)

    def test_user_update_allowed_for_self(self):
        self.client.login(username='owner@example.com', password='pass12345')
        response = self.client.get(reverse('users:user_update', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)

    def test_user_delete_forbidden_for_other_user(self):
        self.client.login(username='other@example.com', password='pass12345')
        response = self.client.post(reverse('users:user_delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_user_delete_allowed_for_self(self):
        self.client.login(username='owner@example.com', password='pass12345')
        response = self.client.post(reverse('users:user_delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_password_reset_request_rejects_unknown_email(self):
        # PasswordResetRequestForm.clean_email() validates the email exists,
        # so an unknown email re-renders the form with an error (not a crash).
        response = self.client.post(reverse('users:password_reset'), {
            'email': 'nobody@example.com',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'не найден')
