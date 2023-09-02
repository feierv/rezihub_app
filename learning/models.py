from django.db import models

from authentication.models import User
from django.db.models import Count


class Question(models.Model):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
    DIFICULTIES = (
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    )
    uuid = models.CharField(max_length=50, unique=True)
    content = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    dificulty = models.CharField(
        choices=DIFICULTIES,
        max_length=30,
        default=EASY,
        help_text='ex: Easy')
    page_nr = models.ManyToManyField('PageNr')
    has_multiple_answers = models.BooleanField()
    correct_answers = models.ManyToManyField('Answer',
                                              related_name='correct_answers')
    @property
    def answers(self):
        return Answer.objects.filter(question=self)
    
    def __str__(self):
        return f'question from {self.category.name} from pages: {[p.number for p in self.page_nr.all()]}'

    

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=50, unique=True)
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    general_category = models.ForeignKey('GeneralCategory', on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    
class GeneralCategory(models.Model):
    KUMAR = 'Kumar'
    CHIRURGIE = 'Chirurgie'
    SINOPSIS = 'Sinopsis'
    NAMES = (
        (KUMAR, 'Kumar'),
        (CHIRURGIE, 'Chirurgie'),
        (SINOPSIS, 'Sinopsis'),
    )
    name = models.CharField(
        choices=NAMES,
        max_length=30,
        unique=True,
        default=KUMAR,
        help_text='ex: Kumar')

    def __str__(self):
        return self.name


class PageNr(models.Model):
    number = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.number)


class LearningSessionQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answers = models.ManyToManyField(Answer, null=True)
    is_correct = models.BooleanField(null=True)

    @property
    def correct_answers(self):
        return self.question.correct_answers
    
    @property
    def answers(self):
        return self.question.answers
    
    def __str__(self):
        return f'session question of {self.question.id}, {self.question.content}'


class LearningSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    questions = models.ManyToManyField(LearningSessionQuestion)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'session of {self.user.email}'
    
    @property
    def last_unanswered_question(self):
        unanswered_questions = self.questions.filter(user_answers=None)
        return unanswered_questions.first()

    @property
    def total_questions(self):
        return self.questions.all().count()

    @property
    def answered_questions(self):
        # wrong and correct
        return self.questions.annotate(answer_count=Count('user_answers')).filter(answer_count__gt=0).count()


    @property
    def statistics(self):
        return f'{self.answered_questions}/{self.total_questions}'
    
    @property
    def chapter_name(self):
        return self.category.name
    
    @property
    def completion_percentage(self):
        if self.total_questions == 0:
            return '0 %'  # Avoid division by zero error
        percentage = (self.answered_questions / self.total_questions) * 100
        return '{:.1f} %'.format(percentage)