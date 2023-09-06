from django.db import models

from authentication.models import User
from django.db.models import Count, Sum


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
    points = models.IntegerField(default=0)

    @property
    def pages(self):
        return self.question.page_nr.values_list('number', flat=True)

    @property
    def multiple(self):
        return self.question.has_multiple_answers

    @property
    def correct_answers(self):
        return self.question.correct_answers.all().values_list('id', flat=True)
    
    @property
    def answers(self):
        return self.question.answers.all()
    
    def __str__(self):
        return f'session question of {self.question.id}, {self.question.content}'


class LearningSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    questions = models.ManyToManyField(LearningSessionQuestion)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f'session of {self.user.email}'
    
    def calculate_points(self, correct_answers, user_answers):
        """
        Calculează punctajul pentru răspunsurile furnizate de utilizatori în funcție de răspunsurile corecte.

        Args:
            correct_answers (dict): Un dicționar cu întrebări corecte și răspunsurile aferente.
            user_answers (dict): Un dicționar cu întrebări furnizate de utilizator și răspunsurile aferente.

        Returns:
            int: Punctajul obținut de utilizator în funcție de răspunsurile sale.
        """
        # Funcție internă pentru a calcula numărul de răspunsuri corecte și greșite furnizate de utilizator
        def get_user_correct_answers_and_wrong_answers():
            correct_count = sum(1 for item in user_answers if item in correct_answers)
            different_count = len(user_answers) - correct_count
            return correct_count,  different_count

        # Punctajul inițial este 0
        points = 0

        # Numărul de răspunsuri corecte în răspunsurile furnizate de utilizator
        correct_answers_count = len(correct_answers)
        # correct_answers = [int(answ) for answ in correct_answers]
        # Verificăm dacă există mai multe răspunsuri corecte sau doar unul singur
        is_multiple_correct_answers = correct_answers_count > 1

        # Calculăm numărul de răspunsuri corecte și greșite furnizate de utilizator
        user_correct_count, wrong_answers = get_user_correct_answers_and_wrong_answers()

        if is_multiple_correct_answers:
            # Pentru întrebări cu răspuns multiplu
            max_points = 5
            if user_correct_count > 0:
                # Adăugăm puncte pentru răspunsurile corecte
                points += user_correct_count
            if wrong_answers > 0:
                # Scădem puncte pentru răspunsurile incorecte
                points += (max_points - wrong_answers) - correct_answers_count
            else:
                # Dacă nu sunt răspunsuri incorecte, se adaugă restul punctelor
                points += max_points - correct_answers_count
        else:
            # Pentru întrebări cu un singur răspuns corect
            points = 4 if user_correct_count == correct_answers_count and wrong_answers == 0 else 0

        return points    
    
    def get_previous_question(self, indexes_to_deduct):
        questions = list(self.questions.all().values_list('id', flat=True))
        last_unanswered_question = self.last_unanswered_question
        if not last_unanswered_question: 
            last_unanswered_question = self.questions.last()
        actual_qustion_id = self.last_unanswered_question.id if self.last_unanswered_question \
                else last_unanswered_question.id
        previous_position_index = questions.index(actual_qustion_id) - indexes_to_deduct
       
        previous_question_id = questions[previous_position_index]
        question_instance = self.questions.get(id=previous_question_id)
        return question_instance

    @property
    def session_points(self):
        return 0
    
    @property
    def is_first(self):
        return self.last_unanswered_question == self.questions.all().first()

    @property
    def last_unanswered_question(self):
        unanswered_questions = self.questions.filter(user_answers=None)
        return unanswered_questions.first()

    @property
    def total_questions(self):
        return self.questions.all().count()
    
    @property
    def total_points(self):
        points = self.questions.aggregate(
            total_points=Sum('points'))['total_points']
        return points or 0

    @property
    def answered_questions(self):
        # wrong and correct
        return self.questions.annotate(
            answer_count=Count('user_answers')).filter(answer_count__gt=0).count()

    @property
    def statistics(self):
        return f'{self.answered_questions + 1}/{self.total_questions}'
    
    @property
    def chapter_name(self):
        return self.category.name
    
    @property
    def completion_percentage(self):
        if self.total_questions == 0:
            return '0 %'  # Avoid division by zero error
        percentage = (self.answered_questions / self.total_questions) * 100
        return '{:.1f} %'.format(percentage)