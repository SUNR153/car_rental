from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Car
from modeltranslation.admin import TranslationAdmin

@admin.register(Car)
class CarAdmin(TranslationAdmin):
    list_display = ('brand', 'model', 'year', 'price_per_day', 'location', 'category', 'is_available')
    list_filter = ('category', 'is_available', 'location')
    search_fields = ('brand', 'model', 'location')
    list_editable = ('is_available',)

