from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator

from authentication.decorators import login_required_decorator
from django.views import View

from dashboard.form import TodoTaskForm

# Create your views here.

class DashboardView(View):
    template_name = 'dashboard/index.html'

    @method_decorator(login_required_decorator)
    def get(self, request):
        user = request.user
        context = dict(
            user=user
        )
        return render(request, self.template_name, context)


class TodoView(View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        form = TodoTaskForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TodoTaskForm(request.POST, request_user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            print()
            print('Debugger: ', form.errors)
            print()
        return render(request, self.template_name, {'form': form})
