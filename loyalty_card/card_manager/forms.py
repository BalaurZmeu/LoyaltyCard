from django import forms
from .models import Card

class CardSearchForm(forms.Form):
    series = forms.CharField(required=False, label='Series')
    id_number = forms.CharField(required=False, label='Number')
    issued = forms.DateField(required=False, widget=forms.SelectDateWidget, label='Issued')
    expires = forms.DateField(required=False, widget=forms.SelectDateWidget, label='Expires')
    status = forms.ChoiceField(choices=[('', '---')]+list(Card.CARD_STATUS), required=False, label='Status')

