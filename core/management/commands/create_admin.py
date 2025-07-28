from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates an admin user if not exists'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = 'Pragin'
        password = 'Rajavisa1'
        email = 'pragin.T.dev@gmail.com'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created'))
        else:
            self.stdout.write(f'Superuser "{username}" already exists')
