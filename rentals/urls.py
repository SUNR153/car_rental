from django.urls import path
from . import views

app_name = 'rentals'

urlpatterns = [
    path('', views.rental_list, name='rental_list'),
    path('my_rentals/', views.my_rental, name='my_rental'),
    path('<int:pk>/', views.rental_detail, name='rental_detail'),
    path('create/<int:car_id>/', views.rental_create, name='rental_create'),
    path('<int:pk>/edit/', views.rental_update, name='rental_update'),
    path('<int:pk>/delete/', views.rental_delete, name='rental_delete'),
    path('<int:pk>/extend/', views.rental_extend, name='rental_extend'),
    path('owner/', views.owner_rentals, name='owner_rentals'),
]
