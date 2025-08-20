from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

@login_required
def notification_list(request):
    notifications = request.user.notifications.all()
    data = [
        {
            "actor": n.actor.username,
            "verb": n.verb,
            "timestamp": n.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "is_read": n.is_read,
        }
        for n in notifications
    ]
    return JsonResponse(data, safe=False)
