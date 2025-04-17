from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = f'{self.cleaned_data['first_name']}{self.cleaned_data['email']}'
        if commit:
            user.save()
        return user
    
    def clean_password(self):
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')

        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError('check password')
        return pass2
    
    def clean_name(self):
        return self.cleaned_data['first_name']
    
    def clean_surname(self):
        return self.cleaned_data['last_name']
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['phone'].widget.attrs['placeholder'] = 'phone'
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        self.fields['password2'].widget.attrs['placeholder'] = 'password'
        
        self.fields['password1'].widget.attrs['id'] = 'password-input'
        self.fields['password2'].widget.attrs['id'] = 'password-input'
    
class UserLoginForm(forms.Form):
    email = forms.EmailField(label = 'email', required=True, max_length=254)
    password = forms.CharField(label='paassword', widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('incorrecr password or email')
        return self.cleaned_data
    
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'email'
        self.fields['password'].widget.attrs['placeholder'] = 'password'
        
        self.fields['password'].widget.attrs['id'] = 'password-input'