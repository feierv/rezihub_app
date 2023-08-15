from django.urls import path, include
from authentication import views


urlpatterns = [
    path('register/', views.SendRegisterEmailView.as_view(), name='register'),
    path('continue-register/', views.ContinueRegisterView.as_view(),
         name='continue-register'),
    path('login/', views.CustomLogInView.as_view(), name='login'),

]
