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
        label='New activation period',
        widget=forms.Select(
            attrs={
                'style': 'width: 160px;',
                'class': 'form-control',
            }
        )
    )


class CardGeneratorForm(forms.Form):
    series = forms.CharField(
        required=True, 
        label='Series',
        widget=forms.TextInput(
            attrs={
                'style': 'width: 300px;',
                'class': 'form-control',
            }
        )
    ) 
    
    expires = forms.ChoiceField(
        choices=[
            ('1', '1 month'),
            ('6', '6 months'),
            ('12', '12 months'),
        ],
        required=False,
        label='New activation period',
        widget=forms.Select(
            attrs={
                'style': 'width: 300px;',
                'class': 'form-control',
            }
        )
    )
    
    quantity = forms.IntegerField(
        required=True,
        label='Quantity',
        min_value=1,
        max_value=500,
        widget=forms.NumberInput(
            attrs={
                'style': 'width: 300px;',
                'class': 'form-control',
            }
        )
    )

