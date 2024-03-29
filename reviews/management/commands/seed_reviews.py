import random

from django.core.management.base import BaseCommand

from django_seed import Seed

from users.models import User
from reviews.models import Review
from rooms import models as room_models


class Command(BaseCommand):

    help = "This command creates reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many reviews do you want ro create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(Review, number, {
            "accuracy": lambda x: random.randint(0, 5),
            "communication": lambda x: random.randint(0, 5),
            "cleanliness": lambda x: random.randint(0, 5),
            "location": lambda x: random.randint(0, 5),
            "check_in": lambda x: random.randint(0, 5),
            "value": lambda x: random.randint(0, 5),
            "room": lambda x: random.choice(rooms),
            "user": lambda x: random.choice(all_users)
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reviews created!"))
