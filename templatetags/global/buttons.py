# buttons.py

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
    return f"""
        <!-- Start of primary button -->
        <button class='button button--primary'>{text}</button>
        <!-- End of primary button -->
    """

@register.simple_tag  
def google_button(text):
    """
    Generates a Google styled button.

    :param text: The text displayed on the button.
    :return: HTML markup for the Google button.

    <!-- Usage of google_button template tag -->
    {% google_button "Sign in with Google" %}
    """
    return f"""
        <!-- Start of Google button -->
        <button class='button button--google'>
             <span><i class="fa-brands fa-google"></i> {text}</span>
        </button>
        <!-- End of Google button -->
    """
  
@register.simple_tag
def secondary_button(text):
    """
    Generates a secondary styled button with an arrow icon.

    :param text: The text displayed on the button.
    :return: HTML markup for the secondary button.

    <!-- Usage of secondary_button template tag -->
    {% secondary_button "Go Back" %}
    """
    return f"""
        <!-- Start of secondary button -->
        <button class='button button--secondary'>
            <span><i class="fa-solid fa-arrow-left"></i> {text}</span>
        </button>
        <!-- End of secondary button -->
    """

