from django.db import models
from django.conf import settings 
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Notification(models.Model):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # <-- use this instead of auth.User
        related_name='notifications_sent',
        on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # <-- use this instead of auth.User
        related_name='notifications_received',
        on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.actor} {self.verb} {self.recipient}"
