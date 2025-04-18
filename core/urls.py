from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),                # http://127.0.0.1:8000/
    path('about/', views.about, name='about'),          # http://127.0.0.1:8000/about/
    path('contact/', views.contact, name='contact'),    # http://127.0.0.1:8000/contact/
]

