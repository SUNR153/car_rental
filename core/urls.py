from django.urls import path
#from .views import *
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.about, name='about'),
    path('', views.contact, name='contact'),
]
