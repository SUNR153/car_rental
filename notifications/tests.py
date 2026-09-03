from django.contrib.auth import get_user_model
from django.test import TestCase

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
