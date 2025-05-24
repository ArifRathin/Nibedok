from django.shortcuts import render
from .models import NotificationType, Notification


def allNotifications(request):
    notifications = Notification.objects.filter(notif_for=request.user).order_by('-updated_at')
    data = {
        'notifications':notifications
    }
    return render(request, 'notifications.html', data)