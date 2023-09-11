from django.utils import timezone

from factory.django import DjangoModelFactory
from factory import SubFactory
from factory.faker import Faker

from tests.base import BaseFactory


class UserFactory(DjangoModelFactory, BaseFactory):
    email = Faker('email')
    username = Faker('user_name')
    password = 'a@123456'
    is_verified = True
    is_active = True
    is_superuser = False
    is_staff = False
    is_hidden = False

    last_used_ip = Faker('ipv4')
    last_login = timezone.now()
    date_joined = timezone.now()

    class Meta:
        model = 'identity.User'


class UserBanFactory(DjangoModelFactory, BaseFactory):
    user = SubFactory(UserFactory)
    until = timezone.now() + timezone.timedelta(hours=1)
    reason = 'Test'

    class Meta:
        model = 'identity.UserBan'