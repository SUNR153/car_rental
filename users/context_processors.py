from notifications.models import Notification  # Предполагаю, что у вас есть модель Notification

def unread_notifications_count(request):
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
    else:
        unread_count = 0
    return {'unread_notifications_count': unread_count}