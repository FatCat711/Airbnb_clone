from django.db import models
from django.utils import timezone

from core import models as core_models


class Reservation(core_models.TimeStampedModel):

    """Reservation Model Definition"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRM = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRM, "Confirm"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(choices=STATUS_CHOICES, max_length=12, default=STATUS_PENDING)
    guest = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reservations")
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE, related_name="reservations")
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"{self.room.name} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return self.check_in < now < self.check_out
    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out
    is_finished.boolean = True
