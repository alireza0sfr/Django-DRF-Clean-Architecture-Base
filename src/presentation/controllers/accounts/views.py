from djoser.views import UserViewSet

from infrastructure.repositories.accounts.user import UserRepository


class AuthenticationViewSet(UserViewSet):
    queryset = UserRepository().get_all()
