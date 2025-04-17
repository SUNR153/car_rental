from django.shortcuts import render, redirect, get_object_or_404
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from .form import RegistrationForm, UserCreationForm, UserLoginForm

User = get_user_model()

def profile(request):
    return render(request, 'users/profile.html')

def user_list(request):
    users = User.objects.all()
    return render(request, 'users/users_list.html', {'users': users})

def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/users_details.html', {'user': user})

def user_create(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users/')
    else:
        form = UserCreationForm()
    return render(request, 'users/users_create.html', {'form': form})

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserCreationForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect(f'/users/{pk}/')
    return render(request, 'users/users_update.html', {'form': form})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('/users/')
    return render(request, 'users/users_delete.html', {'user': user})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.get(email=email)
            login(request, user)
            return redirect('/')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/login/')
    return render(request, 'users/logout.html')