from random import choices
from string import ascii_uppercase as letters
from .models import Card


def generate_series():
    """This function generates a unique two uppercase letters series."""
    while True:
        new_series = ''.join(choices(letters, k=2))
        if not Card.objects.filter(series=new_series).exists():
            return new_series

