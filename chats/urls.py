from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
    path('<int:car_id>/', views.chat_view, name='chat_view'),
    path('my_chats/', views.my_chats, name='my_chats'),
    path('api/messages/<int:chat_id>/', views.fetch_messages, name='fetch_messages'),
    path('api/messages/<int:chat_id>/', views.api_messages, name='api_messages'),
    path('api/send_message/<int:chat_id>/', views.api_send_message, name='api_send_message'),
]