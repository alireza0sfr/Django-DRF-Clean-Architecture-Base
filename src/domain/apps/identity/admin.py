from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ModelForm, CharField, PasswordInput
from django.utils.translation import gettext_lazy as _

from infrastructure.exceptions.exceptions import PasswordMissmatchException

from .models import UserBan, IPBan

User = get_user_model()

class UserCreationForm(ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = CharField(label="Password", widget=PasswordInput)
    password2 = CharField(label="Password confirmation", widget=PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_verified', 'is_superuser', 'is_staff', 'is_hidden']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise PasswordMissmatchException()
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_verified', 'is_superuser', 'is_staff', 'is_hidden']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format(
                f"../../{self.instance.pk}/password/"
            )

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
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
