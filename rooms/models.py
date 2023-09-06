from django.db import models
from django_countries.fields import CountryField
from django.urls import reverse

from core import models as core_models
from users import models as user_model


class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    """Room type Definition"""
    class Meta:
        verbose_name = "Room Type"
        verbose_name_plural = "Room types"
        ordering = ["name"]


class Amenity(AbstractItem):
    """Amenity Model Definition"""
    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """Facility Model Definition"""
    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """HouseRule Model Definition"""
    class Meta:
        verbose_name = "House Rule"
        verbose_name_plural = "House Rules"


def room_photo_directory_path(instance: "Photo", filename: str) -> str:
    return f"rooms/room_{instance.room.id}/photos/{filename}"


class Photo(core_models.TimeStampedModel):

    """Photo model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="rooms_photos")
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name="photos")

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    guests = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(user_model.User, on_delete=models.CASCADE, related_name="rooms")
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True, related_name="rooms")
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="rooms")
    facilities = models.ManyToManyField(Facility, blank=True, related_name="rooms")
    house_rules = models.ManyToManyField(HouseRule, blank=True, related_name="rooms")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = self.city.title()
        super().save(*args, **kwargs)

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_avg()
            return round(all_ratings/len(all_reviews), 2)
        return 0

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def first_photo(self):
        try:
            photo, = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_photos(self):
        photos = self.photos.all()[1:5]
        return photos
