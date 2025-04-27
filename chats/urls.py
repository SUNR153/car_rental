# chats/urls.py
from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
    path('<int:car_id>/', views.chat_view, name='chat_view'),
    path('my_chats/', views.my_chats, name='my_chats'),
]