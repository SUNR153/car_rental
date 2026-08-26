from django.urls import path
from . import views

app_name = 'favorites'

urlpatterns = [
    path('', views.favorites_list, name='favorites_list'),
    path('add/<int:car_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove/<int:car_id>/', views.remove_from_favorites, name='remove_from_favorites'),
]
