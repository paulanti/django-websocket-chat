from django.urls import path

from .views import *

app_name = 'chat'
urlpatterns = [
    # {% url('chat:list') %}
    path('', chat_rooms_list_view, name='list'),
    # {% url('chat:list') pk %}
    path('<int:pk>/', chat_room_detail_view, name='detail')
]
