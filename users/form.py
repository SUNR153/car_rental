from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate
from .models import Profile, PasswordResetCode
import uuid

User = get_user_model()

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'id': 'password-input'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'id': 'password-input'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone'}),
            'drivers_license': forms.Select(choices=[('Yes'), ('No')])
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = f"{self.cleaned_data['first_name']}_{self.cleaned_data['email'].split('@')[0]}"
        if commit:
            user.set_password(self.cleaned_data["password1"])
            user.save()
            Profile.objects.create(
                user=user,
                phone=user.phone,
                driver_license=self.cleaned_data['driver_license'])
        return user

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'id': 'email-input'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'id': 'password-input'
    }))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('Incorrect email or password.')
        return self.cleaned_data

class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'driver_license']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone']

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email не найден.")
        return email

class PasswordResetConfirmForm(forms.Form):
    code = forms.CharField(label="Код", max_length=36)
    new_password = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            uuid_obj = uuid.UUID(code)
            reset_code = PasswordResetCode.objects.get(code=uuid_obj)
            if reset_code.is_expired():
                raise forms.ValidationError("Код истёк. Запросите новый.")
        except (ValueError, PasswordResetCode.DoesNotExist):
            raise forms.ValidationError("Неверный код.")
        return code

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data