from django.urls import path
from .views import UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView

app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='list'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('create/', UserCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', UserUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
]
