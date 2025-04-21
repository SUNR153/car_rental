from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .form import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .token import TokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.utils import timezone
from django.contrib.auth import login as auth_login, authenticate, logout
from users.models import Profile
from django.contrib import messages

User = get_user_model()
acc_activ_token = TokenGenerator()

def profile(request):
    return render(request, 'users/profile.html', {
        'u': request.user
    })

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

def del_inactive_users():
    check_time = timezone.now() - timezone.timedelta(minutes=15)
    inactive_users = User.objects.filter(is_active = False, date_joined__lt = check_time)

    for user in inactive_users:
        user.delete()

def register_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')

        # Проверка: есть ли уже такой номер
        if Profile.objects.filter(phone=phone).exists():
            messages.error(request, 'Этот номер телефона уже используется.')
            return render(request, 'users/register.html')

    if request.method != "POST":
        del_inactive_users()
        form =  RegistrationForm()
    else:
        del_inactive_users()
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                exist_user = User.objects.get(email=email)
                if not exist_user.is_active():
                    exist_user.delete()
                else:
                    return render(request, '#', {'error': 'This user already exists'})
            except:
                pass

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Link to activate your account on the website ' + str(current_site)
            messege = render_to_string('usesrs/acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': acc_activ_token.make_token(user),
            })
            to_email = email
            email = EmailMessage(mail_subject, messege, to=[to_email])
            email.send()
            return render(request, 'users/register_email_message.html', {"email": to_email})

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

@login_required
def profile_settings(request):
    profile = request.user.profile
    settings_form = ProfileSettingsForm(request.POST or None, request.FILES or None, instance=profile)
    password_form = PasswordChangeForm(user=request.user, data=request.POST or None)

    if request.method == 'POST':
        if 'save_settings' in request.POST and settings_form.is_valid():
            settings_form.save()
            return redirect('users:settings')

        if 'change_password' in request.POST and password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, request.user)
            return redirect('users:settings')

    return render(request, 'users/settings.html', {
        'settings_form': settings_form,
        'password_form': password_form
    })

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
@login_required
def toggle_theme(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        request.user.profile.theme = data.get('theme', 'light')
        request.user.profile.save()
        return JsonResponse({'status': 'ok'})

from django.views.decorators.csrf import csrf_protect
from django.utils.translation import activate
from django.contrib.auth.decorators import login_required
#from django.shortcuts import redirect
from users.models import Profile

@csrf_protect
@login_required
def change_language(request):
    if request.method == 'POST':
        lang = request.POST.get('language')
        if lang in ['ru', 'en', 'kz']:
            # Создаём профиль, если не существует
            if not hasattr(request.user, 'profile'):
                Profile.objects.create(user=request.user, phone=getattr(request.user, 'phone', ''))

            request.user.profile.language = lang
            request.user.profile.save()

            # Переключаем язык и сохраняем в сессии
            activate(lang)
            request.session['django_language'] = lang  # Используем строку напрямую

    return redirect(request.META.get('HTTP_REFERER', '/'))
