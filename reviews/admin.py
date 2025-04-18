from django.contrib import admin
from .models import Review

# Register your models here.

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('car__brand', 'author__username', 'comment')