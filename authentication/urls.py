from django.urls import path, include
from authentication import views


urlpatterns = [
    path('send-register-email/', views.SendRegisterEmailView.as_view(), name='register'),
    path('continue-register/', views.ContinueRegisterView.as_view(), name='continue-register'),
]