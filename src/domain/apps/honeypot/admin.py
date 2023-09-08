from django.contrib import admin
from .models import Honeypot

class LoginAttemptAdmin(admin.ModelAdmin):
    model = Honeypot
    list_display = ('id', 'username', 'ip', 'path', 'created_date')
    search_fields = list_display
    list_filter = ('username',)
    ordering = ('id', 'username', 'ip', 'path', 'created_date')

admin.site.register(Honeypot,LoginAttemptAdmin)
