from django.shortcuts import redirect, render
from django.views import View
from app.settings import ORDERED_ORDER, PAGE_NUMBER_ORDER, RANDOM_ORDER
from learning.models import Category, GeneralCategory, LearningSession, LearningSessionQuestion, Question
from django.utils.decorators import method_decorator
from authentication.decorators import learning_session_started_decorator, login_required_decorator
import random
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Count, Case, When, IntegerField, OuterRef, Subquery, ExpressionWrapper, FloatField, F, Q


# Create your views here.

class ChapterSelectView(View):
    template_name = 'learning/index.html'
    sub_categories_template_name = 'learning/components/sub-categories.html'

    @method_decorator(login_required_decorator)
    # @method_decorator(learning_session_started_decorator)

    def get(self, request, category_id=None):
        def format_context(categories):
            context = {'categories': []}
            
            for category in categories:
                completion_percentage = 0
                
                active_learning_session = LearningSession.objects.filter(
                    category=category,
                    is_completed=False
                ).last()

                if not active_learning_session:
                    active_learning_session = LearningSession.objects.filter(
                        category=category,
                        is_completed=True
                    ).last()
                    completion_percentage = 100 if active_learning_session else 0
                else:
                    if active_learning_session.total_questions == 0:
                        completion_percentage = 0
                    else:
                        completion_percentage = ( active_learning_session.answered_questions
                                    / active_learning_session.total_questions) * 100
                context['categories'].append((category, completion_percentage))
            return context


        if not category_id:
            general_categories = GeneralCategory.objects.all()
            kumar_categories = general_categories.filter(
                name=GeneralCategory.KUMAR).first().category_set.all()
            context = format_context(kumar_categories)
            context['general_categories'] = general_categories
            return render(request, self.template_name , context)

        categories = GeneralCategory.objects.get(
                id=category_id).category_set.all()
        context = format_context(categories)
        return render(request, self.sub_categories_template_name  , context)

class NavigateBetweenCompletedQuestionsView(View):
    template_name = 'learning/views/session-view.html'
    component_name = 'learning/components/session-component.html'
    completed_component = 'learning/components/completed-question-component.html'

    def get(self, request):
        def format_previous_data(completed=False):
            answered_questions = progress.answered_questions
            if not progress.last_unanswered_question:
                answered_questions -= 1
            percentage = ((answered_questions - indexes_to_deduct) / 
                        progress.total_questions) * 100
            percentage = '{:.1f} %'.format(percentage)
            statistics = f'{answered_questions + 1 - indexes_to_deduct}/{progress.total_questions}'
            if completed:
                statistics = f'{answered_questions - indexes_to_deduct}/{progress.total_questions}'
               
            user_answers = question.user_answers.values_list('id', flat=True)
            return dict(
                category=dict(name=progress.category),
                last_unanswered_question=dict(multiple=question.multiple),
                question_content=question.question.content,
                completion_percentage=percentage,
                correct_answers=question.correct_answers,
                statistics=statistics,
                user_answers=user_answers,
                points=question.points,
            )
        user = request.user
        progress = user.progress
        indexes_to_deduct = int(request.GET.get('indexes_to_deduct'))
        print()
        print()
        print('* * * * * * * ')
        print(indexes_to_deduct)
        print('* * * * * * * ')
        print()
        print()
        question = progress.get_previous_question(indexes_to_deduct)
        is_completed = False
        if progress.has_all_questions_answered:
            is_completed = True
            data = format_previous_data(True)
        else:
            data = format_previous_data()
        context = dict(
            progress_obj = data,
            question = question,
        )
        response_data = {
            'html_content': render_to_string(self.completed_component, context),
            'percentage': data['completion_percentage']
        }
        is_first = question == progress.questions.all().first()
        is_actual = question == progress.last_unanswered_question
        is_last = question == progress.questions.all().last()
        if is_first:
            response_data['is_first'] = is_first
        if is_actual:
            context = dict(
                progress_obj = progress,
                question = question,
            )
            response_data = {
            'html_content': render_to_string(self.component_name, context),
            }
            response_data['is_actual'] = is_actual
            response_data['is_last'] = is_last
            if is_completed:
                response_data = {
                'html_content': render_to_string(self.completed_component, context),
                }
            response_data['is_actual'] = is_actual
            response_data['is_last'] = is_last
            response_data['percentage'] = progress.completion_percentage
        
        return JsonResponse(response_data)


class CompleteSessionView(View):
        session_complete = 'learning/components/learning-completed.html'
        
        @method_decorator(login_required_decorator)
        def post(self, request, session_id=None):
            user = request.user
            session = user.learningsession_set.filter(id=session_id, is_completed=False).last()
            session.is_completed = True
            session.save()
            # context = dict(total_points=session.total_points)
            response_data = {
                            'html_content': render_to_string(self.session_complete, {}),
                            "total_points": session.total_points
                            }
            return JsonResponse(response_data)
            # return render(request, self.session_complete, context)


class LastLearningSessionView(View):
        @method_decorator(login_required_decorator)
        def get(self, request):
            user = request.user
            session = user.learningsession_set.filter(is_completed=False).last()
            exists = dict(session_id=session.id) if session else False
            return JsonResponse(dict(exists=exists))


class LearningSessionView(View):
        template_name = 'learning/views/session-view.html'
        component_name = 'learning/components/session-component.html'
        session_complete = 'learning/components/learning-completed.html'

        @method_decorator(login_required_decorator)
        def get(self, request, session_id=None):
            user = request.user
            session = user.learningsession_set.filter(is_completed=False,
                                                      id=session_id).first()

            get_component = request.GET.get('get_component', None)
            if session:
                if session.has_all_questions_answered:
                    context = dict(
                        progress_obj=session,
                        question=session.last_unanswered_question,
                        is_completed = True
                    )
                    return render(request, self.template_name, context)
                else:
                    context = dict(
                        progress_obj=session,
                        percentage=session.completion_percentage,
                    )
                    if get_component:
                        if session.last_unanswered_question == session.questions.last():
                            response_data = {
                                'html_content': render_to_string(self.component_name, context),
                                'percentage': session.completion_percentage,
                                "is_last": True
                            }
                            return JsonResponse(response_data)
                        response_data = {
                                'html_content': render_to_string(self.component_name, context),
                                'percentage': session.completion_percentage,
                                "is_last": False
                            }
                        return JsonResponse(response_data)
                        # return render(request, self.component_name, context)
                    if session.last_unanswered_question == session.questions.last():
                        context['is_last'] = True
                    return render(request, self.template_name, context)
            # return JsonResponse(dict(session_exist=False))
            return redirect('chapter-select')
        
        @method_decorator(login_required_decorator)
        def post(self, request, session_id=None):
            def check_if_question_is_correct():
                if question.multiple:
                    question.is_correct = True if  user_answers == question.correct_answers else False
                else:
                    question.is_correct = False if points == 0 else True

            user = request.user
            user_answers = request.POST.getlist('answers[]')
            user_answers = [int(ans) for ans in user_answers]
            session = user.learningsession_set.filter(id=session_id).first()
            question = session.last_unanswered_question
            points = session.calculate_points(
            question.correct_answers,
                user_answers)
            question.points += points
            question.user_answers.add(*user_answers)
            check_if_question_is_correct()
            question.save()
            answers = [str(element) for element in session.last_unanswered_question.correct_answers]
            data = {
                'new_answers': answers,
                'points': points,
                'total_points': session.total_points,
            }
            return JsonResponse(data)
        

            
class StartLearningSessionView(View):
    @method_decorator(login_required_decorator)
    def post(self, request):
        def create_session():
            category = Category.objects.get(id=category_id)
            LearningSession.objects.filter(category=category,
                                            is_completed=False).update(is_completed=True)
            session = LearningSession.objects.create(
                user=user,
                category=Category.objects.get(id=category_id),
            )
            session.questions.add(*questions)
            session.save()
            return session.id

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
        session_id = create_session()
        data = dict(status=200,
                    session_id=session_id)
        return JsonResponse(data)

        
