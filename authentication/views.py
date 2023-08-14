from django.shortcuts import render, redirect
from django.views import View
from authentication.models import User
from django.contrib.auth import login
from  authentication.forms import RegisterForm
from authentication.utils import calculate_remaining_hours, get_step_form, hash_password, send_email, create_register_token
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta, timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

class SendRegisterEmailView(View):
    template_name = 'authentication/send-register-email.html'

    def get(self, request):
        # Check if the user is already logged in
        if request.user.is_authenticated:
            return redirect('/dashboard')  # Redirect to the dashboard view

        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # Check if the user is already logged in
        if request.user.is_authenticated:
            return redirect('/dashboard')  # Redirect to the dashboard view

        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('continue-register')
        return render(request, self.template_name, {'form': form})

class ContinueRegisterView(View):
    template_name = 'authentication/continue-register.html'

    def get(self, request):
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
