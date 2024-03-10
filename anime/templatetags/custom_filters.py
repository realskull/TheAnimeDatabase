from django import template

register = template.Library()

@register.filter(name='clean_genre')
def clean_genre(genre_string):
    # Remove unwanted characters
    cleaned_genre = genre_string[2:-2].split("', '")
    return ", ".join(cleaned_genre)
