from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.utils import timezone
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse
from django.utils.translation import activate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.contrib.auth.tokens import default_token_generator
from django.utils.timezone import now, timedelta

from .form import RegistrationForm, UserLoginForm, ProfileSettingsForm
from .models import Profile
from .token import TokenGenerator

User = get_user_model()
acc_activ_token = TokenGenerator()

# 🔹 User Profile Page
@login_required
def profile(request):
    return render(request, 'users/profile.html', {'u': request.user})

# 🔹 View all users (admin use)
def user_list(request):
    users = User.objects.all()
    return render(request, 'users/users_list.html', {'users': users})

# 🔹 View single user (admin use)
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/users_details.html', {'user': user})

# 🔹 Create user (admin use)
def user_create(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('users:user_list')
    return render(request, 'users/users_create.html', {'form': form})

# 🔹 Update user (admin use)
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = RegistrationForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('users:user_detail', pk=pk)
    return render(request, 'users/users_update.html', {'form': form})

# 🔹 Delete user (admin use)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('users:user_list')
    return render(request, 'users/users_delete.html', {'user': user})

# 🔹 Auto-delete inactive users
def delete_inactive_users():
    limit = timezone.now() - timezone.timedelta(minutes=15)
    User.objects.filter(is_active=False, date_joined__lt=limit).delete()

# 🔹 Registration with email activation
@csrf_protect
def register_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if Profile.objects.filter(phone=phone).exists():
            messages.error(request, 'This phone number is already in use.')
            return render(request, 'users/register.html')

    delete_inactive_users()

    if request.method != 'POST':
        form = RegistrationForm()
    else:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                existing_user = User.objects.get(email=email)
                if not existing_user.is_active:
                    existing_user.delete()
                else:
                    return render(request, 'users/register.html', {'error': 'This user already exists.'})
            except User.DoesNotExist:
                pass

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = f'Activate your account on {current_site.domain}'
            message = render_to_string('users/acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': acc_activ_token.make_token(user),
            })

            email_obj = EmailMessage(subject, message, to=[email])
            email_obj.send()
            return render(request, 'users/register_email_message.html', {"email": email})

    return render(request, 'users/register.html', {'form': form})

# 🔹 Login view
def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'users/login.html', {'form': form})

# 🔹 Logout view
def logout_view(request):
    logout(request)
    return redirect('users:login')

# 🔹 Profile settings (theme, language, password, avatar)
@login_required
def profile_settings(request):
    profile = request.user.profile
    settings_form = ProfileSettingsForm(request.POST or None, request.FILES or None, instance=profile)
    password_form = PasswordChangeForm(request.user, request.POST or None)

    if request.method == 'POST':
        if 'save_settings' in request.POST and settings_form.is_valid():
            settings_form.save()
            messages.success(request, "Settings updated successfully.")
            return redirect('users:settings')

        if 'change_password' in request.POST and password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password changed.")
            return redirect('users:settings')

    return render(request, 'users/settings.html', {
        'settings_form': settings_form,
        'password_form': password_form
    })

# 🔹 AJAX theme toggle (dark/light)
@csrf_exempt
@login_required
def toggle_theme(request):
    if request.method == "POST":
        data = json.loads(request.body)
        theme = data.get("theme")
        if theme in ["light", "dark"]:
            request.user.profile.theme = theme
            request.user.profile.save()
            return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)

# 🔹 Language switcher
@csrf_protect
@login_required
def change_language(request):
    if request.method == 'POST':
        lang = request.POST.get('language')
        if lang in ['ru', 'en', 'kz']:
            if not hasattr(request.user, 'profile'):
                Profile.objects.create(user=request.user, phone=getattr(request.user, 'phone', ''))

            request.user.profile.language = lang
            request.user.profile.save()
            activate(lang)
            request.session['django_language'] = lang

    return redirect(request.META.get('HTTP_REFERER', '/'))

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user:
        if user.is_active:
            return render(request, 'users/fail_activate.html', {'error': 'Account is already activated.'})

        if user and acc_activ_token.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'users/success_activate.html')
        else:
            # токен не прошёл проверку – возможно, истёк
            return render(request, 'users/fail_activate.html', {
                'error': 'Activation link expired. Please register again.'
            })
    else:
        return render(request, 'users/fail_activate.html', {
            'error': 'Invalid activation link.'
        })