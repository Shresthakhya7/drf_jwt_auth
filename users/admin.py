from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_id', 'full_name', 'email', 'contact_number', 'company_name')
    search_fields = ('username', 'email', 'company_name')