import datetime

from django.http import Http404
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from rooms import models as room_models
from . import models
from reviews import forms as review_forms


class CreateError(Exception):
    pass


def create(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year=year, month=month, day=day)
        room = room_models.Room.objects.get(pk=room)
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "Can`t reserve that room")
        return redirect(reverse("core:home"))
    except models.BookedDay.DoesNotExist:
        date_obj = datetime.datetime(year=year, month=month, day=day)
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1)
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation:
            raise Http404()
        if reservation.guest != self.request.user and reservation.room.host != self.request.user:
            raise Http404()
        form = review_forms.CreateReviewForm()
        return render(self.request, "reservations/detail.html",
                      {
                          "reservation": reservation,
                          "form": form
                      })


def edit_reservation(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation:
        raise Http404()
    if reservation.guest != request.user and reservation.room.host != request.user:
        raise Http404()
    if verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRM
    elif verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


def see_reservations(request):
    try:
        _ = request.session["is_hosting"]
        reservations = models.Reservation.objects.filter(room__host=request.user)
        return render(request=request, template_name="reservations/list_guest.html", context={
            "reservations": reservations,
        })
    except KeyError:
        reservations = models.Reservation.objects.filter(guest=request.user)
        return render(request=request, template_name="reservations/list_guest.html", context={
            "reservations": reservations,
        })
