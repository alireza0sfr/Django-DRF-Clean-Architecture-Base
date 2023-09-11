from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()

class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).count() == 0:
            User.objects.create_superuser(
            username=config('SUPERUSER_USERNAME'), password=config('SUPERUSER_PASSWORD'), email=config('SUPERUSER_EMAIL'))
            print('Admin user created!')

        else:
            print('Admin account can only be initialized if no admin account exists!')