from django import forms
import authentication
from authentication.models import City, Speciality, University, User, UserData
from django.contrib.auth.forms import UserCreationForm

from authentication.seed_data import UNIVERSITIES
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

# class RegisterForm(forms.Form):
#     email = forms.EmailField(label='Email', max_length=30, widget=forms.\
#         EmailInput())

class CustomLoginForm(AuthenticationForm):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.TextInput(attrs={"autofocus": True}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False  # Set username field as not required
        self.fields['username'].widget.attrs['autofocus'] = False
        self.error_messages.update({
            'invalid_login': "Please enter a correct email and password. Note that both fields may be case-sensitive."
        })
        
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is False or self.user_cache is None:
                raise self.get_invalid_login_error()
            elif self.user_cache:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class StepOneForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['nume', 'prenume', 'phone', 'localitate', 'judet', 'strada', 'numar']

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super(StepOneForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if self.request_user:
            self.instance.user = self.request_user
        return super(StepOneForm, self).save(commit=commit)

class StepTwoForm(forms.ModelForm):
    class Meta:
        model = User  # Import your User model
        fields = ['university']
    university = forms.ModelChoiceField(queryset=University.objects.all())

class StepThreeForm(forms.ModelForm):
    class Meta:
        model = User  # Import your User model
        fields = ['specialitate']
    specialitate = forms.ModelChoiceField(queryset=Speciality.objects.all())

class StepFourForm(forms.ModelForm):
    class Meta:
        model = User  # Import your User model
        fields = ['oras']
    oras = forms.ModelChoiceField(queryset=City.objects.all())

