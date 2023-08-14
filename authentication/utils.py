from django.core import mail
from app.settings import EMAIL_HOST_USER
import secrets
from datetime import datetime, timedelta, timezone
from django.template.loader import render_to_string

from authentication.forms import StepFourForm, StepOneForm, StepThreeForm, StepTwoForm

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