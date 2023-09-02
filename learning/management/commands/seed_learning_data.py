import re
from django.core.management.base import BaseCommand
from learning.models import *
from learning.test_contstants import KUMAR_LIST

class Command(BaseCommand):
    help = 'Some seeds to populate the database'

    def __create_questions(self, general_category):
        for grid in KUMAR_LIST:
            page_nr_list = [int(nr) for nr in re.findall(r'\d+', grid['page_nr'])]
            category, _ = Category.objects.get_or_create(
                general_category=general_category,
                name=grid['cateogry'])
            q = Question.objects.create(
                      category=category,
                      uuid=grid['uuid'],
                      content=grid['content'],
                      has_multiple_answers=grid['has_multiple_answers'],
                  )
            for page_nr_value in page_nr_list:
                page_nr, created = PageNr.objects.get_or_create(number=page_nr_value)
                q.page_nr.add(page_nr)
            for answ in grid['answers']:
                a = Answer.objects.create(
                    question=q,
                    uuid=answ['uuid'],
                    content=answ['content'],
                )
                if a.uuid in grid['correct_answers']:
                    q.correct_answers.add(a)
    def handle(self, *args, **options):
        kumar, _ = GeneralCategory.objects.get_or_create(name=GeneralCategory.KUMAR)
        chirurgie, _ = GeneralCategory.objects.get_or_create(name=GeneralCategory.CHIRURGIE)
        sinopsis, _ = GeneralCategory.objects.get_or_create(name=GeneralCategory.SINOPSIS)
        self.__create_questions(kumar)


            