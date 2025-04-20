from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'price_per_day', 'is_available']

        widgets = {
            'brand': forms.TextInput(attrs={'placeholder': 'Марка'}),
            'model': forms.TextInput(attrs={'placeholder': 'Модель'}),
            'year': forms.NumberInput(attrs={'placeholder': 'Год'}),
            'price_per_day': forms.NumberInput(attrs={'placeholder': 'Цена за день'}),
            'is_available': forms.CheckboxInput(),
        }
