from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from authentication.decorators import login_required_decorator,  already_logged_in_decorator
from django.contrib.auth import login
from  authentication.forms import CustomLoginForm, RegisterForm
from authentication.utils import  get_step_form, send_email
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.contrib.auth import login


class SendRegisterEmailView(View):
    template_name = 'authentication/send-register-email.html'

    @method_decorator(already_logged_in_decorator) 
    def get(self, request):
        return render(request, self.template_name, None)

    @method_decorator(already_logged_in_decorator) 
    def post(self, request):
        # Check if the user is already logged in
        # if request.user.is_authenticated:
        #     return redirect('/dashboard')  # Redirect to the dashboard view

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

    @method_decorator(login_required_decorator)  # Apply the decorator to the view
    def get(self, request):
            form = get_step_form(request.user.last_uncompleted_step)
            context = {
                'form': form,
            }
            return render(request, self.template_name, context)
    
    @method_decorator(login_required_decorator)  # Apply the decorator to the view
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
            else:
                context['errors'] = form.errors
            return render(request, self.template_name, context)
        else:
            return redirect('/dashboard')
    
    
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
            print("Form errors:", form.non_field_errors())
            print("Form errors:", form.errors)
            non_field_errors = form.non_field_errors()
            if non_field_errors:
                context['non_field_errors'] = non_field_errors
            else:
                context['errors'] = form.errors
        return render(request, self.template_name, context)

    @method_decorator(already_logged_in_decorator) 
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)