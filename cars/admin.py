from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'price_per_day', 'location', 'category', 'is_available')
    list_filter = ('category', 'is_available', 'location')
    search_fields = ('brand', 'model', 'location')
    list_editable = ('is_available',)
