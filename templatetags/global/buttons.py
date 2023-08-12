# buttons.py

from django import template
register = template.Library()

@register.simple_tag
def primary_button(text):
  return f"<button class='auth-form__button auth-form__button--primary'>{text}</button>"

@register.simple_tag  
def secondary_button(text):
  return f"<button class='auth-form__button auth-form__button--secondary'>{text}</button>"
  
@register.simple_tag
def back_button(text):
  return f"<button class='auth-form__button auth-form__button--back'><span><img src='back-arrow.svg'/>{text}</span></button>"
