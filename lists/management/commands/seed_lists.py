import random

from django.core.management.base import BaseCommand

from lists.models import List
from users.models import User
from rooms import models as room_models


class Command(BaseCommand):
    help = "This command creates lists"

    def handle(self, *args, **options):
        users = User.objects.all()
        rooms = room_models.Room.objects.all()

        for user in users:
            list_model = List.objects.create(user=user, name="Favs.")
            to_add = rooms[random.randint(0, 5): random.randint(6, 30)]
            list_model.rooms.add(*to_add)
        self.stdout.write(self.style.SUCCESS(f"lists created!"))
