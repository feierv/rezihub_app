from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.core import serializers
from django.core.serializers import serialize

from authentication.decorators import login_required_decorator
from django.views import View
from authentication.models import TodoTask
from dashboard.form import TodoTaskForm
import json
# Create your views here.

def custom_serialized_response(queryset):
    serialized_data = json.loads(serialize('json', queryset))
    data = []
    for entry in serialized_data:
        obj = queryset.get(pk=entry['pk'])  # Assuming you can retrieve the object using the primary key
        entry['fields']['deadline'] = obj.formatted_deadline  # Replace with your property name
        entry['fields']['deadline_status'] = obj.deadline_status  # Replace with your property name
        data.append(entry)
    return JsonResponse({'tasks': data})

class DashboardView(View):
    template_name = 'dashboard/index.html'

    @method_decorator(login_required_decorator)
    def get(self, request):
        user = request.user
        context = dict(
            user=user
        )
        return render(request, self.template_name, context)


class UpdateTodoView(View):
    template_name = 'dashboard/index.html'

    def post(self, request, todo_id, *args, **kwargs):
        task = TodoTask.objects.get(id=todo_id)
        description = request.POST.get('description', None)
        deadline = request.POST.get('deadline', None)
        task.description = description
        task.deadline = deadline
        task.save()
        return redirect('dashboard')


class GetTodoDetail(View):
    template_name = 'dashboard/index.html'

    def get(self, request, todo_id, *args, **kwargs):
        task = TodoTask.objects.get(id=todo_id)
        serialized_data = serializers.serialize('json', [task])
        serialized_task_list = json.loads(serialized_data)
        serialized_task = serialized_task_list[0]
        return JsonResponse({'task': serialized_task})


class TodoView(View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        form = TodoTaskForm()
        return render(request, self.template_name, {'form': form})
    
    def delete(self, request, todo_id, *args, **kwargs):
        # Access data sent in the DELETE request using request.data
        task = TodoTask.objects.get(id=todo_id)
        task.delete()
        return custom_serialized_response(request.user.todo_tasks)

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
    
    def put(self, request, todo_id, *args, **kwargs):
        def update_is_completed():
            if task.is_completed == False:
                task.is_completed = True
            else:
                task.is_completed = False
        data = json.loads(request.body)
        check = data.get('check', None)
        task = TodoTask.objects.get(id=todo_id)
        if check:
            update_is_completed()
        task.save()
        return custom_serialized_response(request.user.todo_tasks)