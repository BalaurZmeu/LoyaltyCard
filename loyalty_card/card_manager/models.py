from django.db import models
from datetime import datetime
from django.urls import reverse
from .utils import generate_series, generate_id

class Card(models.Model):
    """Model representing a specific loyalty card."""
    
    series = models.CharField(max_length=2, default=generate_series, help_text="Series of the card")
    
    id_number = models.BigIntegerField(
        primary_key=True,
        default=generate_id,
        help_text="Unique ID for this particular card across the whole system"
    )
    
    issued = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(null=True, blank=True)
    last_used = models.DateTimeField(null=True, blank=True)
    amount = models.FloatField(
        default=0,
        help_text="The amount of bonus points granted to a customer"
    )
    
    CARD_STATUS = (
        ('n', 'Not activated'),
        ('a', 'Activated'),
        ('e', 'Expired'),
    )

    status = models.CharField(
        max_length=1,
        choices=CARD_STATUS,
        blank=True,
        default='n',
        help_text="Status of the card",
    )
    
    class Meta:
        ordering = ['series', 'id_number']
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.series} {self.id_number}'
    
    def check_if_expired(self):
        """Determines if the card is expired based on expiration date and current date.
        If card is expired, changes the status of the card to 'expired' and returns True."""
        if self.expires and datetime.now() > self.expires:
            self.status = 'e'
            self.save()
        return self.status == 'e'

    def get_absolute_url(self):
        """Returns the URL to access a particular card instance."""
        return reverse('card-detail', args=[str(self.id_number)])

