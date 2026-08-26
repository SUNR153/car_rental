from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Chat, Message
from cars.models import Car
from notifications.models import Notification
from django.http import JsonResponse
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def chat_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    chat = Chat.objects.filter(car=car, participants=request.user).first()
    if not chat:
        chat = Chat.objects.create(car=car)
        chat.participants.add(request.user, car.author)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(chat=chat, sender=request.user, content=content)
            if request.user != car.author:
                Notification.objects.create(
                    user=car.author,
                    message=f"New message from {request.user.email} about {car.brand} {car.model}"
                )
            return redirect('chats:chat_view', car_id=car_id)

    messages_list = chat.messages.order_by('created_at')

    chat.messages.exclude(sender=request.user).update(is_read=True)

    return render(request, 'chats/chat.html', {
        'chat': chat,
        'messages_list': messages_list,
        'car': car,
    })

@login_required
def my_chats(request):
    chats = Chat.objects.filter(participants=request.user).order_by('-created_at')
    return render(request, 'chats/my_chat.html', {'chats': chats})

@login_required
def fetch_messages(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    messages = chat.messages.order_by('created_at')

    data = []
    for msg in messages:
        data.append({
            'id': msg.id,
            'sender': msg.sender.email,
            'content': msg.content,
            'created_at': msg.created_at.strftime("%d.%m.%Y %H:%M"),
            'is_mine': msg.sender == request.user,
        })
    return JsonResponse({'messages': data})

@login_required
def api_messages(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    messages = chat.messages.order_by('created_at')
    result = []

    for message in messages:
        result.append({
            'id': message.id,
            'sender': message.sender.email,
            'content': message.content,
            'created_at': message.created_at.strftime('%d.%m.%Y %H:%M'),
            'is_mine': message.sender == request.user,
        })

    return JsonResponse({'messages': result})

@csrf_exempt
@login_required
def api_send_message(request, chat_id):
    if request.method == "POST":
        chat = Chat.objects.get(id=chat_id)
        data = json.loads(request.body)
        content = data.get('content')

        if content:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                content=content
            )
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)