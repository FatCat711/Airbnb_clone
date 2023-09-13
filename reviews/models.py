from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """Review model Definition"""

    class Meta:
        ordering = ("-created",)

    review = models.TextField()
    accuracy = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    communication = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    cleanliness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    location = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    check_in = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reviews")
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE, related_name="reviews")

    def rating_avg(self):
        avg = (
            self.accuracy +
            self.communication +
            self.cleanliness +
            self.location +
            self.check_in +
            self.value
        ) / 6
        return round(avg, 2)
    rating_avg.short_description = "avg"

    def __str__(self):
        return f"{self.review} - {self.room}"
