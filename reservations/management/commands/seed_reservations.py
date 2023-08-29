import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from django_seed import Seed

from users.models import User
from reservations.models import Reservation
from rooms import models as room_models


class Command(BaseCommand):
    help = "This command creates reservations"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many reservations do you want ro create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(Reservation, number, {
            "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
            "room": lambda x: random.choice(rooms),
            "guest": lambda x: random.choice(all_users),
            "check_in": lambda x: datetime.now(),
            "check_out": lambda x: datetime.now() + timedelta(days=random.randint(3, 24))
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reservations created!"))
