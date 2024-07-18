from django import forms
from .models import Card

class CardSearchForm(forms.Form):
    series = forms.CharField(required=False, label='Series')
    id_number = forms.CharField(required=False, label='Number')
    issued = forms.DateField(required=False, widget=forms.SelectDateWidget, label='Issued Date')
    expires = forms.DateField(required=False, widget=forms.SelectDateWidget, label='Expiration Date')
    status = forms.ChoiceField(choices=[('', '---')]+list(Card.CARD_STATUS), required=False, label='Status')

