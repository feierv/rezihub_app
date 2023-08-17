import json
from typing import Any
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from authentication.decorators import login_required_decorator,  already_logged_in_decorator
from django.contrib.auth import login
from authentication.forms import CustomLoginForm, RegisterForm
from authentication.models import City, Speciality, University
from authentication.utils import get_specialities_cateogry, get_step_form, get_step_template, send_email
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.contrib.auth import login


class SendRegisterEmailView(View):
    template_name = 'authentication/register.html'

    @method_decorator(already_logged_in_decorator)
    def get(self, request):
        return render(request, self.template_name, None)

    @method_decorator(already_logged_in_decorator)
    def post(self, request):
        form = RegisterForm(request.POST)
        context = {}
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('continue-register')
        else:
            context['errors'] = form.errors
        return render(request, self.template_name, context)


class ContinueRegisterView(View):
    template_name = 'authentication/auth_base.html'

    # Apply the decorator to the view
    @method_decorator(login_required_decorator)
    def get(self, request):
        step = request.user.last_uncompleted_step
        form = get_step_form(step)
        template = get_step_template(step)
        context = {
            'form': form,
        }
        if step == '2':
            universities = University.objects.all().values_list('nume', flat=True)
            context['universities'] = universities
        if step == '3':
            host = request.scheme + "://" + request.get_host()
            speciality_url = host + reverse('specialities')
            specialities = get_specialities_cateogry()
            context['speciality_url'] = speciality_url
            context['specialities'] = specialities
        if step == '4':
            cities = City.objects.all()
            context['cities'] = cities
        return render(request, template , context)

    # Apply the decorator to the view
    @method_decorator(login_required_decorator)
    def post(self, request):
        step = request.user.last_uncompleted_step
        if step:
            context = {}
            form = get_step_form(step)
            data = request.POST.copy()
            data['user'] = request.user.id
            if step == '1':
                form = form(data, request_user=request.user)
            elif step in ['2', '3', '4']:
                form = form(data, instance=request.user)
            context = {
                'form': form,
            }
            if form.is_valid():
                form.save()
                step = request.user.last_uncompleted_step
                form = get_step_form(step)
                context = {
                    'form': form,
                }
            if step == '2':
                universities = University.objects.all().values_list('nume', flat=True)
                context['universities'] = universities
            if step == '3':
                host = request.scheme + "://" + request.get_host()
                speciality_url = host + reverse('specialities')
                specialities = get_specialities_cateogry()
                context['speciality_url'] = speciality_url
                context['specialities'] = specialities
            if step == '4':
                cities = City.objects.all()
                context['cities'] = cities
            else:
                context['errors'] = form.errors
            template = get_step_template(step)
            return render(request, template, context)
        else:
            return redirect('/dashboard')

class GetSpecialitiesView(View):
    def get(self, request):
        STEP_4_TEMPLATE = 'authentication/steps/step4.html'
        specialities_category = request.GET['data']
        specialities = Speciality.objects.filter(category=specialities_category).values_list('nume', flat=True)
        context = {'specialities': specialities}
        return render(request,STEP_4_TEMPLATE , context)


class CustomLogInView(LoginView):
    template_name = 'authentication/login.html'
    form_class = CustomLoginForm

    @method_decorator(already_logged_in_decorator)
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()
        context = dict()
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/dashboard')
        else:
            non_field_errors = form.non_field_errors()
            if non_field_errors:
                context['non_field_errors'] = non_field_errors
            else:
                context['errors'] = form.errors
        return render(request, self.template_name, context)

    @method_decorator(already_logged_in_decorator)
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
