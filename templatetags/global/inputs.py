from django import template
register = template.Library()


"""
Generates a styled text input field for forms.

:param label: The label text for the input field.
:param custom_id: A custom ID for the input element.
:param input_type: The type of input (e.g., 'text', 'email', 'password').
:param placeholder: Optional placeholder text for the input.
:param required: If True, the input will be marked as required.
:param min_length: Minimum character length for the input.
:param max_length: Maximum character length for the input.
:param pattern: Regular expression pattern for input validation.
:param error_message: Custom error message to display when validation fails.
:return: HTML markup for the text input field.

{% text_input "Username" "username" input_type="text" placeholder="Enter your username" required %}
{% text_input "Password" "password" input_type="password" placeholder="Enter your password" required min_length=8 error_message="Password must be at least 8 characters long" %}
{% text_input "Email" "email" input_type="email" placeholder="Enter your email" required pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$" error_message="Please enter a valid email address" %}
"""
@register.simple_tag
def text_input(label, custom_id, input_type='text', placeholder='', required=False, min_length=None, max_length=None, pattern=None, error_message=''):
  input_attrs = f"""
    id='{custom_id}' 
    type='{input_type}' 
    class='form__input' 
    aria-labelledby='{custom_id}-label' 
    placeholder='{placeholder}'
  """
  
  if required:
      input_attrs += " required"
  if min_length is not None:
      input_attrs += f" minlength='{min_length}'"
  if max_length is not None:
      input_attrs += f" maxlength='{max_length}'"
  if pattern is not None:
      input_attrs += f" pattern='{pattern}'"
      
  input_element = f"<input {input_attrs} />"

    return f"""
        <!-- Start of text input field -->
        <div class='form__field'> 
            <label for='{custom_id}' class='form__label'>
                {label}
            </label>
            {input_element}
            <div class='error-message'>{error_message}</div>
        </div>
        <!-- End of text input field -->
    """



@register.simple_tag  
def select_input(label, options=None, required=False, custom_id=None):
    """
    Generates a styled select input field for forms.
    
    :param label: The label text for the input field.
    :param options: A list of dictionaries representing options for the select. Each dictionary should have 'value' and 'text' keys.
    :param required: If True, the input will be marked as required.
    :param custom_id: Optional custom ID for the select input.
    :return: HTML markup for the select input field.

    <!-- Usage of select_input template tag -->
    {% select_input "Select an Option" options=options required custom_id="my-select" %}
    """
    
    if options is None:
        options = []

    select_attrs = f"""
        class='select__input'
        aria-labelledby='{custom_id}-label' 
    """
    
    if custom_id:
        select_attrs += f"id='{custom_id}'"

    # Generate the <select> element with its options
    select_element = f"<select {select_attrs}>"
    for option in options:
        select_element += f"<option value='{option['value']}'>{option['text']}</option>"
    select_element += "</select>"

    return f"""
        <!-- Start of select input field -->
        <div class='select'>
            <label id='{custom_id}-label' class='select__label'>
                {label}
            </label>
            {select_element}
        </div>
        <!-- End of select input field -->
    """
