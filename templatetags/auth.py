from django import template
from django.template.loader import render_to_string

from authentication.forms import StepFourForm, StepThreeForm, StepTwoForm

register = template.Library()


@register.simple_tag
def user_profile_component(form):
    context = {'form': form}

    form_types = [StepTwoForm, StepThreeForm, StepFourForm]
    if type(form) in form_types:
        return render_to_string('authentication/select_component.html', context)
    return render_to_string('authentication/user_profile_component.html', context)
