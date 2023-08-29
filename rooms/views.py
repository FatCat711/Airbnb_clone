from math import ceil
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from django_countries import countries

from rooms import models as room_models
from rooms import forms


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
    paginate_by = 10
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
