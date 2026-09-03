from django.contrib.auth import get_user_model
from django.test import TestCase

from cars.models import Car
from .models import Chat, Message

User = get_user_model()


class ChatModelTests(TestCase):
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

    def test_str_includes_car(self):
        chat = Chat.objects.create(car=self.car)
        self.assertEqual(str(chat), 'Chat for Toyota Camry')

    def test_participants_relation(self):
        chat = Chat.objects.create(car=self.car)
        chat.participants.add(self.owner, self.customer)
        self.assertEqual(chat.participants.count(), 2)
        self.assertIn(chat, self.owner.chats.all())


class MessageModelTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='pass12345',
        )
        self.car = Car.objects.create(
            author=self.owner,
            brand='Toyota',
            model='Camry',
            year=2022,
            price_per_day='50.00',
        )
        self.chat = Chat.objects.create(car=self.car)

    def test_str_includes_sender_and_truncated_content(self):
        message = Message.objects.create(
            chat=self.chat,
            sender=self.owner,
            content='Is this car still available for rent?',
        )
        self.assertEqual(
            str(message),
            'owner@example.com → Toyota Camry: Is this car still av',
        )

    def test_default_unread(self):
        message = Message.objects.create(
            chat=self.chat,
            sender=self.owner,
            content='Hi',
        )
        self.assertFalse(message.is_read)

    def test_related_name_messages(self):
        Message.objects.create(chat=self.chat, sender=self.owner, content='Hi')
        self.assertEqual(self.chat.messages.count(), 1)
        self.assertEqual(self.owner.messages.count(), 1)
