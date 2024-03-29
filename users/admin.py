from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from rooms.models import Room


class RoomInline(admin.StackedInline):
    model = Room


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""

    inlines = [RoomInline]

    fieldsets = UserAdmin.fieldsets + (
        ("Custom Profile", {
            "fields": ("avatar", "gender", "bio",
                       "birthdate", "language", "currency",
                       "superhost", "login_method")
        }),
    )

    list_filter = UserAdmin.list_filter + (
        "superhost",
    )

    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verify",
        "email_secret",
        "login_method",
    ]
