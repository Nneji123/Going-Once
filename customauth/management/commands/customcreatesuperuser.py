from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

import os


class Command(BaseCommand):
    help = "Create a superuser with email and password from .env file"

    def handle(self, *args, **options):
        load_dotenv()  # Load environment variables from .env file
        User = get_user_model()
        email = os.environ.get("SUPERUSER_EMAIL")
        password = os.environ.get("SUPERUSER_PASSWORD")
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS("Superuser created successfully!"))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists!"))
