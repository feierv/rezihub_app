from django import template
register = template.Library()

@register.simple_tag  
def page_title(text):
    """
    Generates a page title with an <h1> heading.

    :param text: The text displayed in the page title.
    :return: HTML markup for the page title.
    <!-- Usage of page_title template tag -->
    {% page_title "Welcome to our Website" %}
    """
    return f"""
        <!-- Page Title -->
        <h1 class='h1__title'>{text}</h1>
    """

@register.simple_tag
def section_title(text):
    """
    Generates a section title with an <h2> heading.

    :param text: The text displayed in the section title.
    :return: HTML markup for the section title.

    <!-- Usage of section_title template tag -->
    {% section_title "Section Introduction" %}
    """
    return f"""
        <!-- Section Title -->
        <h2 class='h2__title-stepper'>{text}</h2>
    """
