import datetime
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
        return self.check_in <= now <= self.check_out
    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        is_finished = now > self.check_out
        if is_finished:
            BookedDay.objects.filter(reservation=self).delete()
        return is_finished
    is_finished.boolean = True

    def save(self, *args, **kwargs):
        if self.pk is None:
            start = self.check_in
            end = self.check_out
            difference = end - start
            existing_booked_day = BookedDay.objects.filter(day__range=(start, end)).exists()
            if not existing_booked_day:
                super().save(*args, **kwargs)
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
                return
        else:
            return super().save(*args, **kwargs)


class BookedDay(core_models.TimeStampedModel):
    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Booked day"
        verbose_name_plural = "Booked days"
