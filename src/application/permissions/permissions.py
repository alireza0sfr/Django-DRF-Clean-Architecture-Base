from rest_framework import permissions


class BasePermission(permissions.BasePermission):
    """ BasePermission class adds all permissions for superUsers """

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_superuser)

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsSuperUser(BasePermission):
    """Allows access only to superusers."""
    def has_object_permission(self, request, view, obj):
        return True

    def has_permission(self, request, view):
        parent_access = super().has_permission(request, view)
        return parent_access or bool(request.user and request.user.is_superuser)


class IsAdminUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        return True

    def has_permission(self, request, view):
        parent_access = super().has_permission(request, view)
        return parent_access or bool(request.user and request.user.is_staff)


class IsOwnerOrReadonly(BasePermission):

    def has_object_permission(self, request, view, obj):
        parent_access = super().has_object_permission(request, view, obj)
        return parent_access or obj.author == request.user.id

    def has_permission(self, request, view):
        return True


class IsAuthenticated(BasePermission):

    def has_object_permission(self, request, view, obj):
        return True

    def has_permission(self, request, view):
        parent_access = super().has_permission(request, view)
        return parent_access or bool(request.user and request.user.is_authenticated)


class IsVerified(BasePermission):

    def has_object_permission(self, request, view, obj):
        parent_access = super().has_object_permission(request, view, obj)
        return parent_access or bool(request.user and request.user.is_verified)

    def has_permission(self, request, view):
        parent_access = super().has_permission(request, view)
        return parent_access or bool(request.user and request.user.is_verified)


class CurrentUserOrAdmin(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        user = request.user
        parent_access = super().has_object_permission(request, view, obj)
        return parent_access or user.is_staff or obj.pk == user.pk

    def has_permission(self, request, view):
        user = request.user
        parent_access = super().has_permission(request, view)
        return parent_access or user.is_staff


class IsAuthenticatedAndIsVerified(IsAuthenticated, IsVerified):
    pass
