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
        if self.users.exists():
            return f'{self.name} ({self.users.count()})'
        return self.name

    class Meta:
        verbose_name = 'Chat room'
        verbose_name_plural = 'Chat rooms'


class Message(TimeStampedModel):
    author = models.ForeignKey(
        verbose_name=_('Author'),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    text = models.TextField(
        verbose_name=_('Text')
    )

    chat = models.ForeignKey(
        verbose_name=_('Chat room'),
        to=ChatRoom,
        on_delete=models.CASCADE
    )

    def get_create_datetime(self):
        return self.created.strftime('%d.%m.%Y %H:%M:%S')

    def __str__(self):
        return f'Message from {self.author} to chat room {self.chat.name}'

    class Meta:
        default_related_name = 'messages'
