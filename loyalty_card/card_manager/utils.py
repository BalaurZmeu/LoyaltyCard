from random import choices, randint
from string import ascii_uppercase as letters


def generate_series():
    """This function generates a two uppercase letters series.
    It will keep generating a new series until it finds one that does
    not already exist in the Card model's series field."""
    # Moved import inside the function to avoid circular import issue
    from .models import Card
    while True:
        new_series = ''.join(choices(letters, k=2))
        if not Card.objects.filter(series=new_series).exists():
            return new_series


def generate_id():
    """This function generates a 10 digits long random integer.
    It will keep generating a new id until it finds one that does
    not already exist in the Card model's id_number field."""
    # Moved import inside the function to avoid circular import issue
    from .models import Card
    while True:
        new_id = randint(10**9, 10**10 - 1)
        if not Card.objects.filter(id_number=new_id).exists():
            return new_id

