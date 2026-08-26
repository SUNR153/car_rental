from django import forms
from .models import Car, CarAvailability
from django.utils.translation import gettext_lazy as _


class CarAvailabilityForm(forms.ModelForm):
    class Meta:
        model = CarAvailability
        fields = ['start_date', 'end_date']
        labels = {
            'start_date': _('Available from'),
            'end_date': _('Available until'),
        }
        help_texts = {
            'start_date': _('The date from which this car is available.'),
            'end_date': _('The date until which this car remains available.'),
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


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
        labels = {
            'brand': _('Brand'),
            'model': _('Model'),
            'year': _('Year'),
            'price_per_day': _('Price per day'),
            'location': _('Location'),
            'category': _('Category'),
            'image': _('Car image'),
            'is_available': _('Is available'),
            'condition': _('Condition'),
            'mileage': _('Mileage (km)'),
            'fuel_type': _('Fuel type'),
            'transmission': _('Transmission'),
            'seats': _('Seats'),
            'features': _('Features'),
        }
        help_texts = {
            'features': _('Enter features separated by commas, e.g. air conditioning, GPS'),
        }
        widgets = {
            'brand': forms.TextInput(attrs={'placeholder': _('Brand')}),
            'model': forms.TextInput(attrs={'placeholder': _('Model')}),
            'year': forms.NumberInput(attrs={'placeholder': _('Year')}),
            'price_per_day': forms.NumberInput(attrs={'placeholder': _('Price per day')}),
            'location': forms.TextInput(attrs={'placeholder': _('City, area')}),
            'category': forms.Select(),
            'image': forms.ClearableFileInput(),
            'is_available': forms.CheckboxInput(),
            'condition': forms.Select(),
            'mileage': forms.NumberInput(attrs={'placeholder': _('e.g. 150000')}),
            'fuel_type': forms.Select(choices=[
                ('petrol', _('Petrol')),
                ('diesel', _('Diesel')),
                ('electric', _('Electric')),
                ('hybrid', _('Hybrid')),
            ]),
            'transmission': forms.Select(choices=[
                ('manual', _('Manual')),
                ('automatic', _('Automatic')),
            ]),
            'seats': forms.NumberInput(attrs={'placeholder': _('Number of seats')}),
            'features': forms.Textarea(attrs={'placeholder': _('Air conditioning, Bluetooth...')}),
        }
