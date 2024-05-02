from django import template

register = template.Library()

@register.filter
def capitalize_first_letter_of_words(value):
    # Split the string into words
    words = value.split()

    # Capitalize the first letter of each word and join them back
    capitalized_words = [word.capitalize() for word in words]
    return ' '.join(capitalized_words)
