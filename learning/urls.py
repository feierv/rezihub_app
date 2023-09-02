from django.urls import path, include
from learning import views


urlpatterns = [
    path('learning-session', views.LearningSessionView.as_view(), name='learning-session'),
    path('start-learning-session', views.StartLearningSessionView.as_view(), name='start-learning-session'),
    path('chapter-select', views.ChapterSelectView.as_view(), name='chapter-select'),
    path('chapter-select/<int:category_id>', views.ChapterSelectView.as_view(),
          name='chapter-select-specific'),
]
