from django.urls import path, include
from dashboard import views


urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('todo-task', views.TodoView.as_view(), name='todo'),
    path('get-todo/<int:todo_id>', views.GetTodoDetail.as_view(), name='get-todo'),
    path('todo-task/<int:todo_id>', views.TodoView.as_view(), name='todo-detail'),
    path('todo-task/<int:todo_id>/delete', views.TodoView.as_view(), name='todo-delete'),
    path('todo/update/<int:todo_id>', views.UpdateTodoView.as_view(), name='update-todo'),
]
