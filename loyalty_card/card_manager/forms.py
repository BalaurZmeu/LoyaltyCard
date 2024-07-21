from django import forms
from .models import Card


class CardSearchForm(forms.Form):
    series = forms.CharField(
        required=False, 
        label='Series',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
    id_number = forms.CharField(
        required=False,
        label='Number',
        widget=forms.TextInput(
            attrs={
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
                'class': 'form-control',
            }
        )
    )
    
    issued = forms.DateField(
        required=False,
        label='Issued',
        widget=forms.SelectDateWidget(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
    expires = forms.DateField(
        required=False,
        label='Expires',
        widget=forms.SelectDateWidget(
            attrs={
                'class': 'form-control',
            }
        )
    )


class ActivateForm(forms.Form):
    expires = forms.ChoiceField(
        choices=[
            ('1', '1 month'),
            ('6', '6 months'),
            ('12', '12 months'),
        ],
        required=False,
        label='Expiration date',
        widget=forms.Select(
            attrs={
                'style': 'width: 150px;',
                'class': 'form-control',
            }
        )
    )

