from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('password_reset_confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.profile_settings, name='settings'),
    path('toggle-theme/', views.toggle_theme, name='toggle-theme'),
    path('change-language/', views.change_language, name='change_language'),
    path('list/', views.user_list, name='user_list'),
    path('create/', views.user_create, name='user_create'),
    path('<int:pk>/', views.user_detail, name='user_detail'),
    path('<int:pk>/edit/', views.user_update, name='user_update'),
    path('<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('map/', views.show_map, name='show_map'),
]
