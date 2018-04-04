from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from model_utils.models import TimeStampedModel


class ChatRoom(TimeStampedModel):
    name = models.CharField(
        verbose_name=_('Chat room name'),
        max_length=255
    )

    users = models.ManyToManyField(
        verbose_name=_('Chat participants'),
        related_name='chats',
        to=settings.AUTH_USER_MODEL,
        blank=True
    )

    def __str__(self):
        return f'{self.name} ({self.users.count()})'

    class Meta:
        verbose_name = 'Chat room'
        verbose_name_plural = 'Chat rooms'
