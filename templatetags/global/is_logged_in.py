from django import template
register = template.Library()


@register.simple_tag
def is_user_logged_in(request):
    return request.user.is_authenticated
