from django.contrib import admin
from .models import Connection

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'status', 'timestamp')
    search_fields = ('sender__username', 'receiver__username')