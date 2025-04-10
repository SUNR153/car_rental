from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.car_list, name='list'),
    path('<int:pk>/', views.car_detail, name='detail'),
    path('create/', views.car_create, name='create'),
    path('<int:pk>/edit/', views.car_update, name='update'),
    path('<int:pk>/delete/', views.car_delete, name='delete'),
]
