from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return
       
        user = get_user_model().objects.filter(email=email).first()
        if user and user.check_password(password):
            return user
