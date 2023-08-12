from django import template
register = template.Library()


@register.simple_tag
def text_input(label):
  return f"<div class='auth-form__field'><label>{label}</label><input type='text' class='auth-form__input'/></div>"

@register.simple_tag  
def select_input(label):
  return f"<div class='select'><label>{label}</label><select class='select__input'><div class='select__icon'></div></select></div>"
