from django.contrib import admin
from django.utils.html import mark_safe
from . import models


class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    inlines = [PhotoInline]

    fieldsets = [
        [
            "Basic Info",
            {
                "fields": ("name", "description", "country", "city", "price", "address")
            }
        ],
        [
            "Times",
            {
                "fields": ["check_in", "check_out", "instant_book"]
            }
        ],
        [
            "Spaces",
            {
                "fields": [
                    "beds",
                    "bedrooms",
                    "baths",
                    "guests",
                ]
            }
        ],
        [
            "More About The Space",
            {
                "classes": ["collapse"],
                "fields": ["amenities",
                           "facilities",
                           "house_rules", ]
            }
        ],
        [
            "Last Details",
            {
                "fields": [
                    "host"
                ]
            }
        ]
    ]

    raw_id_fields = ["host"]

    list_display = [
        "name",
        "name",
        "description",
        "price",
        "address",
        "beds",
        "bedrooms",
        "baths",
        "guests",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    ]

    ordering = [
        "price"
    ]

    list_filter = [
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    ]

    search_fields = [
        "=city",
        "^host__username"
    ]

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "photo counts"

@admin.register(models.RoomType, models.Facility, models.HouseRule, models.Amenity)
class ItemAdmin(admin.ModelAdmin):
    """Item Admin Definition"""

    list_display = [
        "name",
        "used_by"
    ]

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""
    list_display = ["__str__", "get_thumbnail"]

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px"src = "{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"
