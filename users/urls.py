from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # 🔐 Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),

    # 👤 User Profile & Settings
    path('profile/', views.profile, name='profile'),
    path('settings/', views.profile_settings, name='settings'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('change-language/', views.change_language, name='change_language'),

    # ⚙️ User Management (Admin use)
    path('list/', views.user_list, name='user_list'),
    path('create/', views.user_create, name='user_create'),
    path('<int:pk>/', views.user_detail, name='user_detail'),
    path('<int:pk>/edit/', views.user_update, name='user_update'),
    path('<int:pk>/delete/', views.user_delete, name='user_delete'),
]
