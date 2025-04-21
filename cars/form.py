from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'price_per_day', 'is_available']

        widgets = {
            'brand': forms.TextInput(attrs={'placeholder': 'Brand'}),
            'model': forms.TextInput(attrs={'placeholder': 'Model'}),
            'year': forms.NumberInput(attrs={'placeholder': 'Year'}),
            'price_per_day': forms.NumberInput(attrs={'placeholder': 'Price per day'}),
            'is_available': forms.CheckboxInput(),
        }
