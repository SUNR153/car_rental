from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Chat, Message
from cars.models import Car
from notifications.models import Notification

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
            message = Message.objects.create(chat=chat, sender=request.user, content=content)
            if request.user != car.author:
                Notification.objects.create(
                    user=car.author,
                    message=f"New message from {request.user.email} about {car.brand} {car.model}"
                )
            messages.success(request, 'Message sent successfully!')
            return redirect('chats:chat_view', car_id=car_id)

    chat.messages.exclude(sender=request.user).update(is_read=True)

    return render(request, 'chats/chat.html', {'chat': chat, 'car': car})

@login_required
def my_chats(request):
    chats = Chat.objects.filter(participants=request.user).order_by('-created_at')
    return render(request, 'chats/my_chat.html', {'chats': chats})
