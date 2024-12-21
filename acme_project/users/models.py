from django.db import models

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    birthday = models.DateField(
        'День рождения',
        null=True
    )
    bio = models.TextField(
        'Биография',
        null=True
    )
