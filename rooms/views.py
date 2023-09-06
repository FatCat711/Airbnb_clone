from math import ceil
from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, FormView
from django.contrib.messages.views import SuccessMessageMixin

from django_countries import countries

from rooms import models as room_models
from rooms import forms
from users import mixins as user_mixins


# def all_rooms(request: HttpRequest) -> HttpResponse:
#     page = request.GET.get(key="page", default=1)
#     room_list = room_models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)
#     try:
#         rooms = paginator.page(int(page))
#         return render(request=request,
#                       template_name="rooms/room_list.html",
#                       context={
#                           "page": rooms,
#                       })
#
#     except EmptyPage:
#         return redirect("/")

class HomeView(ListView):
    """Home View Definition"""

    model = room_models.Room
    paginate_by = 12
    paginate_orphans = 5
    page_kwarg = "page"
    ordering = "created"
    context_object_name = "rooms"

    # template_name = ""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# def room_detail(request, pk):
#     try:
#         room = room_models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", context={
#             "room": room,
#         })
#     except room_models.Room.DoesNotExist:
#         # return redirect(reverse("core:home"))
#         raise Http404()


class RoomDetail(DetailView):
    """RoomDetail Definition"""
    model = room_models.Room
    template_name = "rooms/detail.html"


def old_search(request):
    city: str = request.GET.get("city", "Anywhere") or "Anywhere"
    city = str.capitalize(city)
    country = request.GET.get(key="country", default="KR") or "KR"
    room_type = int(request.GET.get(key="room_type", default=0))
    price = int(request.GET.get(key="price", default="1"))
    guests = int(request.GET.get(key="guests", default="1"))
    bedrooms = int(request.GET.get(key="bedrooms", default="1"))
    beds = int(request.GET.get(key="beds", default="1"))
    baths = int(request.GET.get(key="baths", default="1"))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist(key="amenities")
    s_facilities = request.GET.getlist(key="facilities")
    form = {
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    room_types = room_models.RoomType.objects.all()
    amenities = room_models.Amenity.objects.all()
    facilities = room_models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,

    }

    filter_args = {}
    if city != "Anywhere":
        filter_args["city__startswith"] = city

    if room_type != 0:
        filter_args["room_type__pk__exact"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if beds != 0:
        filter_args["beds__gte"] = beds

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant:
        filter_args["instant_book"] = True

    if superhost:
        filter_args["host__superhost"] = True

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["amenities__pk"] = int(s_facility)

    filter_args["country"] = country
    rooms = room_models.Room.objects.filter(**filter_args)

    return render(request, "rooms/old_search.html", context={
        **form,
        **choices,
        "rooms": rooms,
    })


class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")

        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book:
                    filter_args["instant_book"] = True

                if superhost:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                filter_args["country"] = country
                qs = room_models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10 , orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(request, "rooms/search.html", context={
                    "form": form,
                    "rooms": rooms,
                })
        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", context={
            "form": form,
        })


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):
    model = room_models.Room
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
    template_name = "rooms/room_edit.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, RoomDetail):
    model = room_models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photos(request, room_pk, photo_pk):
    user = request.user
    try:
        room = room_models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can`t delete that photo")
        else:
            room_models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except room_models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(SuccessMessageMixin, user_mixins.LoggedInOnlyView, UpdateView):
    model = room_models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    fields = [
        "caption",
    ]
    success_message = "Photo Updated"

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):
    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhoto

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(request=self.request, message="Photo Uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):
    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        form.save_m2m()
        messages.success(request=self.request, message="Room Created")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
