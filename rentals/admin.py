from django.contrib import admin
from .models import Rental

# Register your models here.

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('car', 'customer', 'start_date', 'end_date', 'total_price')
    list_filter = ('start_date', 'end_date')
    search_fields = ('car__brand', 'car__model', 'customer__username')