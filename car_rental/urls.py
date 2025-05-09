"""
URL configuration for car_rental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('cars/', include('cars.urls'), name='cars'),
    path('users/', include('users.urls'), name='users'),
    path('reviews/', include('reviews.urls'), name='reviews'),
    path('rentals/', include('rentals.urls'), name='rentals'),
    path('', include('core.urls'), name ='core'),
    path('favorite/', include('favorite.urls'), name='favorite'),
    path('notifications/', include('notifications.urls'), name='notifications'),
    path('chats/', include('chats.urls'), name='chats'),
    #path('', lambda request: redirect('cars:car_list')),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)