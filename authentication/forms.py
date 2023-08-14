from django import forms
from authentication.models import City, Speciality, University, User, UserData
from django.contrib.auth.forms import UserCreationForm

from authentication.seed_data import UNIVERSITIES

# class RegisterForm(forms.Form):
#     email = forms.EmailField(label='Email', max_length=30, widget=forms.\
#         EmailInput())

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