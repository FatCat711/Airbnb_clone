from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.html import strip_tags
import uuid
from django.template.loader import render_to_string

from core import managers as core_managers


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

    LOGIN_EMAIL = "email"
    LOGIN_GH = "github"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GH, "GitHub"),
    )

    avatar = models.ImageField(blank=True, upload_to="users_photos")
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, blank=True, default="Russian")
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, blank=True, default="USD")
    superhost = models.BooleanField(default=False)
    email_verify = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="", blank=True)
    login_method = models.CharField(max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)
    objects = core_managers.CustomUserManager()

    def verify_email(self):
        if self.email_verify is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string("emails/verify_email.html", context={"secret": secret})
            send_mail("Verify Airbnb account",
                      settings.EMAIL_FROM,
                      strip_tags(html_message),
                      [self.email],
                      fail_silently=False,
                      html_message=html_message
                      )
            self.save()
            return

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})
