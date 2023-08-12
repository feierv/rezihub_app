# responsive.py

from django import template
register = template.Library()


"""
####USAGE####
<div class="some-content {% is_mobile %}">
    This content will only be visible on mobile devices.
</div>

<div class="another-content {% is_tablet %}">
    This content will only be visible on tablet devices.
</div>

<div class="yet-another-content {% is_desktop %}">
    This content will only be visible on desktop devices.
</div>

"""
@register.simple_tag
def is_mobile():
    """
    Returns a CSS class based on the screen size for mobile devices.

    :return: CSS class for mobile or empty string for larger screens.
    """
    return "is-mobile"  # You can customize this class name

@register.simple_tag
def is_tablet():
    """
    Returns a CSS class based on the screen size for tablet devices.

    :return: CSS class for tablet or empty string for other screens.
    """
    return "is-tablet"  # You can customize this class name

@register.simple_tag
def is_desktop():
    """
    Returns a CSS class based on the screen size for desktop devices.

    :return: CSS class for desktop or empty string for smaller screens.
    """
    return "is-desktop"  # You can customize this class name
