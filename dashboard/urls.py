from django.urls import path, include
from dashboard import views


urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('todo-task', views.TodoView.as_view(), name='todo'),
]
