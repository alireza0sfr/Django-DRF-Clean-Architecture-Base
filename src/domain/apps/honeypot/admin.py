from django.contrib import admin
from .models import LoginAttempt

class LoginAttemptAdmin(admin.ModelAdmin):
    model = LoginAttempt
    list_display = ('id', 'username', 'ip', 'path', 'created_date')
    search_fields = list_display
    list_filter = ('username',)
    ordering = ('id', 'username', 'ip', 'path', 'created_date')

admin.site.register(LoginAttempt, LoginAttemptAdmin)
