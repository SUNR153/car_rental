from django.urls import path
from . import views

app_name = 'rentals'

urlpatterns = [
    path('', views.rental_list, name='rental_list'),
    path('<int:pk>/', views.rental_detail, name='rental_detail'),
    path('create/', views.rental_create, name='rental_create'),
    path('<int:pk>/edit/', views.rental_update, name='rental_update'),
    path('<int:pk>/delete/', views.rental_delete, name='rental_delete'),
]
