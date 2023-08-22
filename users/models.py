from django.contrib.auth.models import AbstractUser
from django.db import models


def user_avatar_directory_path(instance: "User", filename: str) -> str:
    return f"users/user_{instance.id}/avatar/{filename}"



class User(AbstractUser):

    """Custom User model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_RUSSIAN = "ru"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_RUSSIAN, "Russian"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_RUB = "rub"

    CURRENCY_CHOICES = (
        (CURRENCY_USD, "USD"),
        (CURRENCY_RUB, "RUB")
    )

    avatar = models.ImageField(blank=True, upload_to=user_avatar_directory_path)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, blank=True)
    superhost = models.BooleanField(default=False)
