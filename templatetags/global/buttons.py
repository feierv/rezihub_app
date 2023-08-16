from django.utils.safestring import mark_safe
from django import template
register = template.Library()


@register.simple_tag
def primary_button(text):
    """
    Generates a primary styled button.

    :param text: The text displayed on the button.
    :return: HTML markup for the primary button.

    <!-- Usage of primary_button template tag -->
    {% primary_button "Click me" %}
    """

    button = f"""
        <!-- Start of primary button -->
        <button class='button button--primary'>{text}</button>
        <!-- End of primary button -->
    """
    return mark_safe(button)


@register.simple_tag
def google_button(text):
    """
    Generates a Google styled button.

    :param text: The text displayed on the button.
    :return: HTML markup for the Google button.

    <!-- Usage of google_button template tag -->
    {% google_button "Sign in with Google" %}
    """
    button = f"""
        <!-- Start of Google button -->
        <button class='button button--google'>
             <span><i class="fa-brands fa-google"></i> {text}</span>
        </button>
        <!-- End of Google button -->
    """
    return mark_safe(button)


@register.simple_tag
def secondary_button(text):
    """
    Generates a secondary styled button with an arrow icon.

    :param text: The text displayed on the button.
    :return: HTML markup for the secondary button.

    <!-- Usage of secondary_button template tag -->
    {% secondary_button "Go Back" %}
    """

    button = f"""
        <!-- Start of secondary button -->
        <button class='button button--secondary'>
            <span><i class="fa-solid fa-arrow-left"></i> {text}</span>
        </button>
        <!-- End of secondary button -->
    """
    return mark_safe(button)
