from django.shortcuts import render, redirect
from django.views import View
from authentication.models import User
from django.contrib.auth import login
from  authentication.forms import RegisterForm
from authentication.utils import  get_step_form, send_email
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta, timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

class SendRegisterEmailView(View):
    template_name = 'authentication/send-register-email.html'

    # def get(self, request):
    #     # Check if the user is already logged in
    #     if request.user.is_authenticated:
    #         return redirect('/dashboard')  # Redirect to the dashboard view

    #     form = RegisterForm()
    #     return render(request, self.template_name, {'form': form})
    def get(self, request):
        # Check if the user is already logged in
        # if request.user.is_authenticated:
        #     return redirect('/dashboard')  # Redirect to the dashboard view

        return render(request, self.template_name, None)

    def post(self, request):
        # Check if the user is already logged in
        if request.user.is_authenticated:
            return redirect('/dashboard')  # Redirect to the dashboard view

        form = RegisterForm(request.POST)
        context = {}
        print()
        print(form.is_valid())
        print(form.errors)
        print()
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('continue-register')
        else:
            context['errors'] = form.errors
        return render(request, self.template_name, context)

class ContinueRegisterView(View):
    template_name = 'authentication/auth_base.html'

    def get(self, request):
        print()
        print(request.user.university)
        print()
        if request.user.is_authenticated:  # Check if the user is logged in
            form = get_step_form(request.user.last_uncompleted_step)
            context = {
                'form': form,
            }
            return render(request, self.template_name, context)
        else:
            return redirect('login')  # Redirect to the login page

    def post(self, request):
        if request.user.is_authenticated:  # Check if the user is logged in
            step = request.user.last_uncompleted_step
            if step:
                form = get_step_form(step)
                data = request.POST.copy()
                data['user'] = request.user.id
                if step == '1':
                    form = form(data, request_user=request.user)
                elif step in ['2', '3', '4']:
                    form = form(data, instance=request.user)
                if form.is_valid():
                    form.save()
                step = request.user.last_uncompleted_step
                form = get_step_form(step)
                context = {
                    'form': form,
                }
                return render(request, self.template_name, context)
            else:
                return redirect('/dashboard')
        else:
            return redirect('login')  # Redirect to the login page
    # def get(self, request):
    #     if request.user.is_authenticated:  # Check if the user is logged in
    #         form = get_step_form(request.user.last_uncompleted_step)
    #         context = {
    #             'form': form,
    #         }
    #         return render(request, self.template_name, context)
    #     else:
    #         return redirect('login')  # Redirect to the login page
    
    # def post(self, request):
    #     if request.user.is_authenticated:  # Check if the user is logged in
    #         step = request.user.last_uncompleted_step
    #         if step:
    #             form = get_step_form(step)
    #             data = request.POST.copy()
    #             data['user'] = request.user.id
    #             if step == '1':
    #                 form = form(data, request_user=request.user)
    #             elif step in ['2', '3', '4']:
    #                 form = form(data, instance=request.user)
    #             if form.is_valid():
    #                 form.save()
    #             step = request.user.last_uncompleted_step
    #             form = get_step_form(step)
    #             context = {
    #                 'form': form,
    #             }
    #             return render(request, self.template_name, context)
    #         else:
    #             return redirect('/dashboard')
    #     else:
    #         return redirect('login')  # Redirect to the login page
