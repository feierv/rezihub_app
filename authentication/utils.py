from django.core import mail
from app.settings import EMAIL_HOST_USER
import secrets
from datetime import datetime, timedelta, timezone
from django.template.loader import render_to_string

from authentication.forms import StepFourForm, StepOneForm, StepThreeForm, StepTwoForm
from authentication.models import Speciality

def send_email(token):
        message = f"Acceseaza linku http://127.0.0.1:8000/authentication/continue-register/{token} pt inregistrare"
        # html_body = render_to_string("authentication/reset-password_email-template.html", context)   

        email_from = 'Grile Rezolvate'
        subject = 'Am uitat parola'
        recipient_list = list()
        recipient_list.append('feierv@yahoo.com')

        html_body = "<h1>Email<h1/>"
        msg = mail.EmailMessage(subject,
                                 html_body,
                                   email_from,
                                     recipient_list)
        msg.content_subtype = "html"
        msg.send()

        # mail.send_mail(
        #     'Subject',
        #     message,
        #     EMAIL_HOST,
        #     ['feierv@yahoo.com'],
        #     # fail_silently=False,
        # )

def calculate_remaining_hours(target_datetime):
    current_datetime = datetime.now(timezone.utc)
    
    if current_datetime > target_datetime:
        return 0, 0  # The target datetime has passed
    
    remaining_time = target_datetime - current_datetime - timedelta(hours=9)
    remaining_hours = remaining_time.total_seconds() / 3600

    hours = int(remaining_hours)
    minutes = int((remaining_hours - hours) * 60)
    return hours, minutes

def get_step_form(step):
    forms = {
        '1': StepOneForm,
        '2': StepTwoForm,
        '3': StepThreeForm,
        '4': StepFourForm,
    }
    return forms[step]

def get_step_template(step):
    forms = {
        '1': 'authentication/steps/step1.html',
        '2': 'authentication/steps/step2.html',
        '3': 'authentication/steps/step3.html',
        '4': 'authentication/steps/step5.html',
    }
    return forms[step]


def get_specialities_cateogry():
    assets = [
        dict(
         name='Specialităţi clinice - Adulţi',
         static_url='/static/assets/images/clinice-adulti.png',
         ),
         dict(
         name='Specialităţi clinice - Copii',
         static_url='/static/assets/images/clinice-pediatrice.png',
         ),
         dict(
         name='Specialităţi chirurgicale - Adulţi',
         static_url='/static/assets/images/chirurgicale-adulti.png',
         ),
         dict(
         name='Specialităţi chirurgicale pediatrice',
         static_url='/static/assets/images/chirurgicale-pediatrice.png',
         ),
         dict(
         name='Specialitati paraclinice',
         static_url='/static/assets/images/paraclinice.png',
         ),
    ]
    for category in assets:
        cateogry_name = list(category.values())[0]
        length = Speciality.objects.filter(category=cateogry_name).count()
        category['length'] = length
    return assets
