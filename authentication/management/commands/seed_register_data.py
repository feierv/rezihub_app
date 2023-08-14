from django.core.management.base import BaseCommand
from authentication.seed_data import CITIES, UNIVERSITIES, SPECIALITIES
from authentication.models import Speciality, City, University

class Command(BaseCommand):
    help = 'Some seeds to populate the database'

    def handle(self, *args, **options):
        pass