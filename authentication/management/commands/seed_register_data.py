from django.core.management.base import BaseCommand
from authentication.seed_data import (CITIES,
                                      UNIVERSITIES,
                                      SPECIALITIES_PER_CATEGORY)
from authentication.models import Speciality, City, University

class Command(BaseCommand):
    help = 'Some seeds to populate the database'

    def handle(self, *args, **options):
        for university in UNIVERSITIES:
            University.objects.create(nume=university)
        for city in CITIES:
            City.objects.create(nume=city)
        for category in SPECIALITIES_PER_CATEGORY:
            for category, specialities in category.items():
                for speciality in specialities:
                    Speciality.objects.create(nume=speciality,
                                              category=category)
            