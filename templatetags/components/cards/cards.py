from django import template
register = template.Library()

@register.simple_tag
def speciality_card(img, text):
    """
    Generates a speciality card with an image and text.

    :param img: The image source for the card.
    :param text: The text content of the card.
    :return: HTML markup for the speciality card.

    <!-- Usage of speciality_card template tag -->
    {% speciality_card "image1.jpg" "Speciality 1" %}
    """
    return f"""
        <!-- Speciality Card -->
        <div class='speciality-card'>
            <img class='speciality-card__image' src='{img}'>
            <p class='speciality-card__text'>{text}</p>
        </div>
    """

@register.simple_tag
def sub_speciality_card(img, text):
    """
    Generates a sub-speciality card with an image and text.

    :param img: The image source for the card.
    :param text: The text content of the card.
    :return: HTML markup for the sub-speciality card.

    <!-- Usage of sub_speciality_card template tag -->
    {% sub_speciality_card "image2.jpg" "Sub-Speciality 1" %}

    """
    return f"""
        <!-- Sub-Speciality Card -->
        <div class='sub-speciality-card is-checked'>
            <img class='sub-speciality-card__image' src='{img}'>
            <p class='sub-speciality-card__text'>{text}</p>
        </div>
    """

  