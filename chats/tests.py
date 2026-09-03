import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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


class ChatViewTests(TestCase):
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

    def test_chat_view_requires_login(self):
        response = self.client.get(reverse('chats:chat_view', args=[self.car.pk]))
        self.assertEqual(response.status_code, 302)

    def test_chat_view_creates_chat_with_owner_and_customer(self):
        self.client.login(username='customer@example.com', password='pass12345')
        response = self.client.get(reverse('chats:chat_view', args=[self.car.pk]))
        self.assertEqual(response.status_code, 200)

        chat = Chat.objects.get(car=self.car)
        self.assertIn(self.owner, chat.participants.all())
        self.assertIn(self.customer, chat.participants.all())

    def test_fetch_messages_forbidden_for_non_participant(self):
        chat = Chat.objects.create(car=self.car)
        chat.participants.add(self.owner, self.customer)

        self.client.login(username='stranger@example.com', password='pass12345')
        response = self.client.get(reverse('chats:fetch_messages', args=[chat.pk]))
        self.assertEqual(response.status_code, 404)

    def test_fetch_messages_allowed_for_participant(self):
        chat = Chat.objects.create(car=self.car)
        chat.participants.add(self.owner, self.customer)
        Message.objects.create(chat=chat, sender=self.owner, content='Hi there')

        self.client.login(username='customer@example.com', password='pass12345')
        response = self.client.get(reverse('chats:fetch_messages', args=[chat.pk]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['messages']), 1)

    def test_api_send_message_forbidden_for_non_participant(self):
        chat = Chat.objects.create(car=self.car)
        chat.participants.add(self.owner, self.customer)

        self.client.login(username='stranger@example.com', password='pass12345')
        response = self.client.post(
            reverse('chats:api_send_message', args=[chat.pk]),
            data=json.dumps({'content': 'Hello'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(chat.messages.count(), 0)

    def test_api_send_message_allowed_for_participant(self):
        chat = Chat.objects.create(car=self.car)
        chat.participants.add(self.owner, self.customer)

        self.client.login(username='customer@example.com', password='pass12345')
        response = self.client.post(
            reverse('chats:api_send_message', args=[chat.pk]),
            data=json.dumps({'content': 'Hello'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(chat.messages.count(), 1)
