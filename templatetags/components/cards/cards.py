from django import template
register = template.Library()

@register.simple_tag
def speciality_card(img, text):
  return f"<div class='speciality-card'><img class='speciality-card__image' src='{img}'><p class='speciality-card__text'>{text}</p></div>"

@register.simple_tag
def sub_speciality_card(img, text):
  return f"<div class='sub-speciality-card is-checked'><img class='sub-speciality-card__image' src='{img}'><p class='sub-speciality-card__text'>{text}</p></div>"
  