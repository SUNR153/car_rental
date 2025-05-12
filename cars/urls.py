from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('<int:pk>/', views.car_detail, name='car_detail'),
    path('create/', views.car_create, name='car_create'),
    path('<int:pk>/edit/', views.car_update, name='car_update'),
    path('<int:pk>/delete/', views.car_delete, name='car_delete'),
    path('<int:car_id>/availability/', views.set_availability, name='set_availability'),]
