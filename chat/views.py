from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from chat.models import ChatRoom

__all__ = ['chat_rooms_list_view', 'chat_room_detail_view']


class ChatRoomsListView(LoginRequiredMixin, ListView):
    queryset = ChatRoom.objects.all()
    template_name = 'chat/chat_rooms.html'
    context_object_name = 'chat_rooms'

chat_rooms_list_view = ChatRoomsListView.as_view()


class ChatRoomView(LoginRequiredMixin, DetailView):
    model = ChatRoom
    template_name = 'chat/chat.html'
    context_object_name = 'chat'

chat_room_detail_view = ChatRoomView.as_view()
