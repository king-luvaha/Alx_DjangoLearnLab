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
    
    #Generic foreign key for target object (e.g., post, comment, follow)
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("target_content_type", "target_object_id")

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} {self.verb} {self.target} → {self.recipient}"
