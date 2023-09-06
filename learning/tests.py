from django.test import TestCase
from authentication.models import User
from learning.test_contstants import KUMAR_LIST
from .models import Question, Answer, GeneralCategory, PageNr, LearningSessionQuestion, LearningSession

class QuestionModelTest(TestCase):
    def __create_questions(self, cateogry):
        for grid in KUMAR_LIST:
            q = Question.objects.create(
                      general_category=cateogry,
                      uuid=grid['uuid'],
                      content=grid['content'],
                      category=grid['cateogry'],
                      has_multiple_answers=grid['has_multiple_answers'],
                  )
            for page_nr_value in grid['page_nr']:
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

    def __create_categories(self):
        kumar = GeneralCategory.objects.create(name=GeneralCategory.KUMAR)
        chirurgie = GeneralCategory.objects.create(name=GeneralCategory.CHIRURGIE)
        sinopsis = GeneralCategory.objects.create(name=GeneralCategory.SINOPSIS)
        return kumar ,chirurgie ,sinopsis
    
    def __create_session_questions(self, questions_list):
        return [LearningSessionQuestion.objects.create(question=question)
                for question in questions_list]

    def setUp(self):
        self.categories = self.__create_categories()
        self.__create_questions(self.categories[0])
        self.user = User.objects.create(username='testuser')

    def test__learning_session(self):
        session = LearningSession.objects.create(
            user=self.user
        )
        session_questions = self.__create_session_questions(
            Question.objects.all()[:5])
        session.questions.add(*session_questions)
        q = session.questions.first()
        answ = q.answers[0]
        q.user_answers.add(answ)
        print()
        # print(session.questions.all())
        print(session.last_unanswered_question)
        print()
        

    # def test_session_str_representation(self):
    #     self.assertEqual(str(self.session), f'session of {self.user.email}')

    # Add more test methods to cover other functionalities of your models