from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        'id', 'username', 'email', 'last_login', 'date_joined', 'last_used_ip', 'is_staff', 'is_active', 'is_superuser',
        'is_hidden',
        'is_verified')
    list_filter = list_display
    search_fields = ('id', 'email', 'username')
    ordering = search_fields
    fieldsets = (
        ('Authentication', {'fields': ('username', 'email', 'password')}),
        ('Permission', {'fields': ('is_staff', 'is_active', 'is_superuser', 'is_hidden', 'is_verified')}),
        ('Group Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Metadata', {'fields': ('last_login', 'date_joined', 'last_used_ip')}),

    )
    add_fieldsets = (
        ('Authentication', {'fields': ('username', 'email', 'password1', 'password2')}),
        ('Permission', {'fields': ('is_staff', 'is_active', 'is_superuser', 'is_hidden', 'is_verified')}),
        ('Meta Data', {'fields': ('date_joined',)})
    )

    def save_form(self, request, form, change):
        if not change:

            if form.cleaned_data['is_superuser']:
                form.instance = self.model.objects.create_superuser(form.cleaned_data['username'],
                                                                    form.cleaned_data['email'],
                                                                    form.cleaned_data['password1'])

            else:
                form.instance = self.model.objects.create_user(form.cleaned_data['username'],
                                                               form.cleaned_data['email'],
                                                               form.cleaned_data['password1'])
        return super().save_form(request, form, change)


admin.site.register(User, CustomUserAdmin)
