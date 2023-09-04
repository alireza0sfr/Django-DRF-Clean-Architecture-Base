from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone

from .models import UserBan, IPBan

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


class IsActiveFilter(admin.SimpleListFilter):
    title = 'Is Active'
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (
            ('True', True),
            ('False', False),
        )

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(until__gt=timezone.now())
        if self.value() == 'False':
            return queryset.filter(until__lte=timezone.now())


class CustomUserBanAdmin(admin.ModelAdmin):
    model = UserBan
    list_display = ('id', 'user', 'reason', 'active', 'description', 'until', 'created_date')
    search_fields = list_display
    list_filter = ('user__username', 'reason', IsActiveFilter)
    ordering = ('id', 'user', 'reason', 'until', 'created_date')

    @admin.display(empty_value=False)
    def active(self, obj):
        return obj.is_active

    active.boolean = True  # Display as a boolean (checkbox)


class CustomIPBanAdmin(admin.ModelAdmin):
    model = IPBan
    list_display = ('id', 'ip', 'reason', 'active', 'description', 'until', 'created_date')
    search_fields = list_display
    list_filter = ('ip', 'reason', IsActiveFilter)
    ordering = ('id', 'reason', 'until', 'created_date')

    @admin.display(empty_value=False)
    def active(self, obj):
        return obj.is_active

    active.boolean = True  # Display as a boolean (checkbox)


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserBan, CustomUserBanAdmin)
admin.site.register(IPBan, CustomIPBanAdmin)
