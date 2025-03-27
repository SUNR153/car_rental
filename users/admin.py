from django.contrib import admin
from .models import *

@admin.register(User)
class CustomPostAdmin(admin.ModelAdmin):
    fieldsets = (
            #
    )
    add_fieldsets = (
            #
    )
    list_display = ()
    search_fields = ()
    ordering = ()
    def get_fieldsets(self, request, obj = None):
        if obj:
            return self.fieldsets
        return self.add_fieldsets
#admin.site.register(User)