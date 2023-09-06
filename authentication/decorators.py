from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

# Define the decorator
def login_required_decorator(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.last_uncompleted_step:
                if request.path == reverse('dashboard'):
                    return redirect('continue-register')
                return view_func(request, *args, **kwargs)
            else:
                if request.path == reverse('dashboard') or request.path != reverse('continue-register'):
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect('dashboard')
        return redirect('login')
    return _wrapped_view

def already_logged_in_decorator(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.last_uncompleted_step:
                return redirect('continue-register')
            else:
                return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def learning_session_started_decorator(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.progress:
            return redirect('learning-session')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
