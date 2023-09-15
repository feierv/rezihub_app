from django.urls import path, include
from learning import views


urlpatterns = [
    path('last-session', views.LastLearningSessionView.as_view(), name='last-session'),
    path('learning-session/<int:session_id>/', views.LearningSessionView.as_view(), name='learning-session'),
    path('complete-session/<int:session_id>/', views.CompleteSessionView.as_view(), name='complete-session'),
    path('start-learning-session', views.StartLearningSessionView.as_view(), name='start-learning-session'),
    path('chapter-select', views.ChapterSelectView.as_view(), name='chapter-select'),
    path('navigate-between-completed-questions/', views.NavigateBetweenCompletedQuestionsView.as_view(), name='navigate'),
    path('chapter-select/<int:category_id>', views.ChapterSelectView.as_view(),
          name='chapter-select-specific'),
]
