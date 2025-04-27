from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications_list(request):
    notifications = request.user.notifications.order_by('-created_at')
    return render(request, 'notifications/notifications_list.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications:list')

@login_required
def mark_all_as_read(request):
    request.user.notifications.update(is_read=True)
    return redirect('notifications:list')
