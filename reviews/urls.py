from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('<int:car_id>/', views.review_list, name='review_list'),
    path('my_review/', views.my_review, name='my_review'),
    path('<int:pk>/', views.review_detail, name='review_detail'),
    path('create/', views.review_create, name='review_create'),
    path('<int:pk>/edit/', views.review_update, name='review_update'),
    path('<int:pk>/delete/', views.review_delete, name='review_delete'),
    
]
