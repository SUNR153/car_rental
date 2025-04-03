from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

User = get_user_model()

class UserListView(ListView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'users'

class UserDetailView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'

class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:list')

class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email', 'role']
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:list')


class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:list')
