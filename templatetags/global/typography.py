from django import template
register = template.Library()

@register.simple_tag  
def page_title(text):
  return f"<h1 class='auth__title'>{text}</h1>"
  
@register.simple_tag
def section_title(text):
  return f"<h2 class='auth__title-stepper'>{text}</h2>"