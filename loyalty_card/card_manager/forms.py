from django import forms
from .models import Card

class CardSearchForm(forms.Form):
    series = forms.CharField(
        required=False, 
        label='Series',
        widget=forms.TextInput(
            attrs={
                'style': 'width: 300px;',
                'class': 'form-control',
            }
        )
    )
    
    id_number = forms.CharField(
        required=False,
        label='Number',
        widget=forms.TextInput(
            attrs={
                'style': 'width: 300px;',
                'class': 'form-control',
            }
        )
    )
    
    status = forms.ChoiceField(
        choices=[('', '---')]+list(Card.CARD_STATUS),
        required=False,
        label='Status',
        widget=forms.Select(
            attrs={
                'style': 'width: 300px;',
                'class': 'form-control',
            }
        )
    )
    
    issued = forms.DateField(
        required=False,
        label='Issued',
        widget=forms.SelectDateWidget(
            attrs={
                'style': 'width: 300px;',
                'class': 'form-control',
            }
        )
    )
    
    expires = forms.DateField(
        required=False,
        label='Expires',
        widget=forms.SelectDateWidget(
            attrs={
                'style': 'width: 300px;',
                'class': 'form-control',
            }
        )
    )

