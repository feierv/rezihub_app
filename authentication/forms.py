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
    university = forms.CharField()  
    class Meta:
        model = User  # Import your User model
        fields = ['university']

    def clean(self):
        cleaned_data = super().clean()
        university = cleaned_data.get('university')
        # Retrieve the University object based on the provided name
        try:
            university = University.objects.get(nume=university)
        except University.DoesNotExist:
            raise forms.ValidationError("Invalid university selected.")
        
        cleaned_data['university'] = university
        return cleaned_data


class StepThreeForm(forms.ModelForm):
    specialitate = forms.CharField()  
    class Meta:
        model = User  # Import your User model
        fields = ['specialitate']

    def clean(self):
        cleaned_data = super().clean()
        specialitate = cleaned_data.get('specialitate')
        # Retrieve the University object based on the provided name
        try:
            speciality = Speciality.objects.get(nume=specialitate)
        except Speciality.DoesNotExist:
            raise forms.ValidationError("Invalid speciality selected.")
        
        cleaned_data['specialitate'] = speciality
        return cleaned_data


class StepFourForm(forms.ModelForm):
    oras = forms.CharField()  
    class Meta:
        model = User  # Import your User model
        fields = ['oras']

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get('oras')
        
        # Retrieve the University object based on the provided name
        try:
            city = City.objects.get(nume=city)
        except City.DoesNotExist:
            raise forms.ValidationError("Invalid city selected.")
        
        cleaned_data['oras'] = city
        return cleaned_data
    