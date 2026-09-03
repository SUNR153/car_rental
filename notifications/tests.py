from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Notification

User = get_user_model()


class NotificationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alice',
            email='alice@example.com',
            password='pass12345',
        )

    def test_str_truncates_message(self):
        notification = Notification.objects.create(
            user=self.user,
            message='This is a fairly long notification message that should be truncated',
        )
        self.assertEqual(
            str(notification),
            'alice@example.com - This is a fairly long notifica',
        )

    def test_default_is_unread(self):
        notification = Notification.objects.create(
            user=self.user,
            message='Hello',
        )
        self.assertFalse(notification.is_read)

    def test_related_name_notifications(self):
        Notification.objects.create(user=self.user, message='One')
        Notification.objects.create(user=self.user, message='Two')
        self.assertEqual(self.user.notifications.count(), 2)


class NotificationViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alice',
            email='alice@example.com',
            password='pass12345',
        )
        self.other_user = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='pass12345',
        )

    def test_mark_as_read_requires_login(self):
        notification = Notification.objects.create(user=self.user, message='Hi')
        response = self.client.get(reverse('notifications:mark_as_read', args=[notification.pk]))
        self.assertEqual(response.status_code, 302)

    def test_mark_as_read_marks_own_notification(self):
        notification = Notification.objects.create(user=self.user, message='Hi')
        self.client.login(username='alice@example.com', password='pass12345')
        self.client.get(reverse('notifications:mark_as_read', args=[notification.pk]))
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_mark_as_read_returns_404_for_other_users_notification(self):
        notification = Notification.objects.create(user=self.other_user, message='Hi')
        self.client.login(username='alice@example.com', password='pass12345')
        response = self.client.get(reverse('notifications:mark_as_read', args=[notification.pk]))
        self.assertEqual(response.status_code, 404)

    def test_mark_all_as_read(self):
        Notification.objects.create(user=self.user, message='One')
        Notification.objects.create(user=self.user, message='Two')
        self.client.login(username='alice@example.com', password='pass12345')
        self.client.get(reverse('notifications:mark_all_as_read'))
        self.assertEqual(self.user.notifications.filter(is_read=False).count(), 0)
