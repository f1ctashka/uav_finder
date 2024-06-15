from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Gender(models.TextChoices):
        male = "male"
        female = "female"

    email = models.EmailField(max_length=255, unique=True)
    gender = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        choices=Gender.choices,
        default=Gender.male,
    )
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
