from django import forms

from django_countries.fields import CountryField

from . import models


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="RU").formfield()
    room_type = forms.ModelChoiceField(required=False,
                                       empty_label="Any kind",
                                       queryset=models.RoomType.objects.all())
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(queryset=models.Amenity.objects.all(),
                                               widget=forms.CheckboxSelectMultiple,
                                               required=False,
                                               )
    facilities = forms.ModelMultipleChoiceField(queryset=models.Facility.objects.all(),
                                                widget=forms.CheckboxSelectMultiple,
                                                required=False,
                                                )


class CreatePhoto(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = [
            "caption",
            "file",
        ]

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        photo.room = models.Room.objects.get(pk=pk)
        photo.save()


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = [
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "beds",
            "bedrooms",
            "baths",
            "guests",
            "instant_book",
            "room_type",
            "amenities",
            "facilities",
            "house_rules",
            "check_in",
            "check_out",
        ]

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        return room
