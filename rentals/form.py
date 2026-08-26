from django import forms
from .models import Rental

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['car', 'customer', 'start_date', 'end_date', 'total_price']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'total_price': forms.NumberInput(attrs={'placeholder': 'Total price'}),
        }
