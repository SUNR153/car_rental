from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
        'brand', 'model', 'year',
        'price_per_day', 'location',
        'category', 'image', 'is_available',
        'condition', 'mileage', 'fuel_type',
        'transmission', 'seats', 'features'
        ]
        widgets = {
        'brand': forms.TextInput(attrs={'placeholder': 'Brand'}),
        'model': forms.TextInput(attrs={'placeholder': 'Model'}),
        'year': forms.NumberInput(attrs={'placeholder': 'Year'}),
        'price_per_day': forms.NumberInput(attrs={'placeholder': 'Price per day'}),
        'location': forms.TextInput(attrs={'placeholder': 'Location'}),
        'category': forms.Select(),
        'image': forms.ClearableFileInput(),
        'is_available': forms.CheckboxInput(),
        'condition': forms.TextInput(attrs={'placeholder': 'Condition'}),
        'mileage': forms.NumberInput(attrs={'placeholder': 'Mileage in km'}),
        'fuel_type': forms.Select(choices=[('petrol', 'Petrol'), ('diesel', 'Diesel'), 
                                        ('electric', 'Electric'), ('hybrid', 'Hybrid')]),
        'transmission': forms.Select(choices=[('manual', 'Manual'), ('automatic', 'Automatic')]),
        'seats': forms.NumberInput(attrs={'placeholder': 'Number of seats'}),
        'features': forms.Textarea(attrs={'placeholder': 'Enter features separated by commas'}),
        }
