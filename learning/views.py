from django.shortcuts import redirect, render
from django.views import View
from app.settings import ORDERED_ORDER, PAGE_NUMBER_ORDER, RANDOM_ORDER
from learning.models import Category, GeneralCategory, LearningSession, LearningSessionQuestion, Question
from django.utils.decorators import method_decorator
from authentication.decorators import learning_session_started_decorator, login_required_decorator
import random
from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.

class ChapterSelectView(View):
    template_name = 'learning/index.html'
    sub_categories_template_name = 'learning/components/sub-categories.html'

    @method_decorator(login_required_decorator)
    @method_decorator(learning_session_started_decorator)

    def get(self, request, category_id=None):
        if not category_id:
            general_categories = GeneralCategory.objects.all()
            kumar_categories = general_categories.filter(
                name=GeneralCategory.KUMAR).first().category_set.all()
            context = {'general_categories': general_categories,
                    'categories': kumar_categories}
            return render(request, self.template_name  , context)
        
        categories = GeneralCategory.objects.get(
                id=category_id).category_set.all()
        context = {'categories': categories}
        return render(request, self.sub_categories_template_name  , context)


class NavigateBetweenCompletedQuestionsView(View):
    template_name = 'learning/components/navigate-component.html'
    component_name = 'learning/components/learning-component.html'

    def get(self, request, direction=None):
        def format_previous_data():
            answered_questions = progress.answered_questions
            if not progress.last_unanswered_question:
                answered_questions -= 1
            percentage = ((answered_questions - indexes_to_deduct) / 
                        progress.total_questions) * 100
            percentage = '{:.1f} %'.format(percentage)
            statistics = f'{answered_questions + 1 - indexes_to_deduct}/{progress.total_questions}'
            user_answers = question.user_answers.values_list('id', flat=True)
            return dict(
                category_name=progress.category,
                question_content=question.question.content,
                is_mulitple = question.multiple,
                completion_percentage=percentage,
                correct_answers=question.correct_answers,
                statistics=statistics,
                answers=question.answers,
                user_answers=user_answers,
                points=question.points,
            )

        user = request.user
        progress = user.progress
        indexes_to_deduct = int(request.GET.get('indexes_to_deduct'))
        if int(indexes_to_deduct) == 0 and progress.last_unanswered_question:
            context = dict(
                progress_obj = request.user.progress,
                last_question = request.user.progress.last_unanswered_question,
                )
            response_data = {
            'html_content': render_to_string(self.component_name, context),
            'is_first': False,
            'is_last': True,
            'is_all_completed': progress.last_unanswered_question is None,
            }
            return JsonResponse(response_data)
        question = progress.get_previous_question(indexes_to_deduct)
        question.refresh_from_db()
        context = format_previous_data()
        is_first = question == progress.questions.all().first()
        is_last = question == progress.questions.all().last()
        response_data = {
            'html_content': render_to_string(self.template_name, context),
            'is_first': is_first,
            'is_last': is_last,
            'is_all_completed': progress.last_unanswered_question is None,
        }
        return JsonResponse(response_data)


class LearningSessionView(View):
    template_name = 'learning/views/learning-view.html'
    component_name = 'learning/components/learning-component.html'
    learning_completed = 'learning/components/learning-completed.html'

    @method_decorator(login_required_decorator)
    def post(self, request):
        user = request.user
        progress = user.progress
        user_answers = request.POST.getlist('answers[]')
        user_answers = [int(ans) for ans in user_answers]
        question_to_answer = progress.last_unanswered_question
        if question_to_answer:
            points = progress.calculate_points(
                question_to_answer.correct_answers,
                user_answers)
            question_to_answer.points += points
            question_to_answer.user_answers.add(*user_answers)
            question_to_answer.save()
            answers = []
            if progress.last_unanswered_question:
                answers = [str(element) for element in progress.last_unanswered_question.correct_answers]
        return JsonResponse(
            {
             'new_answers': answers,
             'points': points,
             'total_points': progress.total_points})
            

    @method_decorator(login_required_decorator)
    def get(self, request, flag=None):
        if not request.user.progress:
            return redirect('chapter-select')
        context = dict(
            progress_obj = request.user.progress,
            last_question = request.user.progress.last_unanswered_question,
        )
        if not request.user.progress.last_unanswered_question:
            progress = request.user.progress
            progress.is_completed = True
            progress.save()
            return render(request, self.learning_completed, context)
        if flag == 1:
            context['new_correct_answers'] = request.user.progress.last_unanswered_question.correct_answers
            print(request.user.progress.last_unanswered_question.correct_answers)
            return render(request, self.component_name, context)
        return render(request, self.template_name, context)


class StartLearningSessionView(View):
    @method_decorator(login_required_decorator)
    # @method_decorator(learning_session_started_decorator)
    def post(self, request):
        def create_session():
            session = LearningSession.objects.create(
                user=user,
                category=Category.objects.get(id=category_id),
            )
            session.questions.add(*questions)
            session.save()

        def get_questions_bases_on_learning_type():
            queryset = Category.objects.get(id=category_id).question_set.all()
            if learning_type == RANDOM_ORDER:
                queryset = sorted(queryset, key=lambda x: random.random())
            elif learning_type == PAGE_NUMBER_ORDER:
                queryset = queryset.filter(page_nr__number__in=pages)
            elif learning_type == ORDERED_ORDER:
                queryset = queryset.order_by('page_nr__number', 'id')
            session_questions = [LearningSessionQuestion.objects.create(
                question=question) for question in queryset]
            return session_questions[:4]

        user = request.user
        learning_type = request.POST.get('learning_type')
        category_id = request.POST.get('category_id')
        pages = [request.POST.get('pages[]')]
        questions = get_questions_bases_on_learning_type()
        create_session()
        return redirect('learning-session')
        
