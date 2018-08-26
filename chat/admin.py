from django.contrib import admin

from .models import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', '_users_count', 'created', 'modified')
    readonly_fields = ('_users_count',)
    list_display_links = ('id', 'name')

    def _users_count(self, obj):
        if obj.users.exists():
            return obj.users.count()
        return 0


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'chat', 'text', 'created')
    readonly_fields = ('author', 'text', 'chat')
