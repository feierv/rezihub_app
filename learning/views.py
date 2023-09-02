from django.shortcuts import redirect, render
from django.views import View
from app.settings import ORDERED_ORDER, PAGE_NUMBER_ORDER, RANDOM_ORDER
from learning.models import Category, GeneralCategory, LearningSession, LearningSessionQuestion, Question
from django.utils.decorators import method_decorator
from authentication.decorators import learning_session_started_decorator, login_required_decorator
import random

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


class LearningSessionView(View):
    template_name = 'learning/views/learning-view.html'

    @method_decorator(login_required_decorator)
    def get(self, request):
        print()
        print('!!')
        print()
        return render(request, self.template_name, {})
    


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
            # print()
            # print(user.progress.statistics)
            # print(user.progress.chapter_name)
            # # print(user.progress.chapter_name)
            # print()
            # print(LearningSession.objects.all())
            # print(session)
            # print(session.questions.all())
            # print()
            # LearningSession.objects.all().delete()

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
            return session_questions

        user = request.user
        learning_type = request.POST.get('learning_type')
        category_id = request.POST.get('category_id')
        pages = [request.POST.get('pages[]')]
        questions = get_questions_bases_on_learning_type()
        create_session()
        return redirect('learning-session')
        
