from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate
from .models import Profile

User = get_user_model()

# 🔹 Registration Form
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
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = f"{self.cleaned_data['first_name']}_{self.cleaned_data['email'].split('@')[0]}"
        if commit:
            user.set_password(self.cleaned_data["password1"])  # ensures password is hashed
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

# 🔹 Login Form
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

# 🔹 Profile Settings Form
class ProfileSettingsForm(forms.ModelForm):

    LANGUAGE_CHOICES = [
        ('en', '🇺🇸 English'),
        ('ru', '🇷🇺 Russian'),
        ('kz', '🇰🇿 Kazakh'),
    ]

    language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['avatar', 'background', 'language']
