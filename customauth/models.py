from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from .managers import CustomUserManager


class User(AbstractUser, models.Model):
    """
    Custom user model
    """

    username = None  # Set username to None to prevent its creation
    email = models.EmailField(("email address"), unique=True)
    profile_pic = models.ImageField(upload_to="profiles/", blank=True)
    bio = models.TextField(default="This is my Bio.")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
