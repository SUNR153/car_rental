from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['car', 'rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'placeholder': 'Raiting 1-5'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Your comment'}),
        }
