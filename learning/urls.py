from django.urls import path, include
from learning import views


urlpatterns = [
    path('learning-session', views.LearningSessionView.as_view(), name='learning-session'),
    path('learning-session/<int:flag>/', views.LearningSessionView.as_view(), name='learning-session'),
    path('start-learning-session', views.StartLearningSessionView.as_view(), name='start-learning-session'),
    path('chapter-select', views.ChapterSelectView.as_view(), name='chapter-select'),
    path('navigate-between-completed-questions/<str:direction>', views.NavigateBetweenCompletedQuestionsView.as_view(), name='navigate'),
    path('chapter-select/<int:category_id>', views.ChapterSelectView.as_view(),
          name='chapter-select-specific'),
]
