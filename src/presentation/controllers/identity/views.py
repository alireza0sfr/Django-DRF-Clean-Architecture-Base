from djoser.views import UserViewSet

from infrastructure.repositories.identity.user import UserRepository


class AuthenticationViewSet(UserViewSet):
    queryset = UserRepository().get_all()
