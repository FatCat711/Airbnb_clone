from django.contrib import admin
from . import models
from core import models as core_models


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Reservation model Admin"""
    list_display = [
        "id",
        "room",
        "status",
        "check_in",
        "check_out",
        "guest",
        "in_progress",
        "is_finished",
    ]

    list_filter = ["status"]


@admin.register(models.BookedDay)
class BookedDAyAdmin(admin.ModelAdmin):
    list_display = ("day",
                    "reservation",
                    )
