from django.contrib import admin
from .models import Car

# Register your models here.

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'price_per_day', 'is_available')
    list_filter = ('brand', 'year', 'is_available')
    search_fields = ('brand', 'model')