from rest_framework import permissions


class BasePermission(permissions.BasePermission):
    """ BasePermission class adds all permissions for superUsers """

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_superuser)

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class PermissionPolicyMixin:
    def check_permissions(self, request):
        try:
            # This line is heavily inspired from `APIView.dispatch`.
            # It returns the method associated with an endpoint.
            handler = getattr(self, request.method.lower())
        except AttributeError:
            handler = None

        if (
            handler
            and self.permission_classes_per_method
            and self.permission_classes_per_method.get(handler.__name__)
        ):
            self.permission_classes = self.permission_classes_per_method.get(
                handler.__name__)

        super().check_permissions(request)


class IsSuperUser(BasePermission):
    """Allows access only to superusers."""

    def has_permission(self, request, view):
        parent_access = super().has_permission(request, view)
        return parent_access or bool(request.user and request.user.is_superuser)


class isOwnerOrReadonly(BasePermission):

    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        parent_access = super().has_object_permission(request, view, obj)
        return parent_access or obj.author == request.user.id


class IsAuthenticatedAndIsVerified(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_verified
        )
    
    def has_object_permission(self, request, view, obj):
        return True
