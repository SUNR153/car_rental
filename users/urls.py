from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='list'),
    path('<int:pk>/', views.user_detail, name='detail'),
    path('create/', views.user_create, name='create'),
    path('<int:pk>/edit/', views.user_update, name='update'),
    path('<int:pk>/delete/', views.user_delete, name='delete'),
    path('profile/', views.profile, name='profile'),
]
