from django import forms
from.models import *

class CheckoutForm(forms.Form):
    street_name= forms.CharField(label='Street name', max_length=10, widget=forms.TextInput(attrs={'class': 'form-control',
                'placeholder': 'Street name',
                'style': "width: 700px; background: black; color: white; font-family: 'Noto Serif', serif;"
            }))
    apartment_address= forms.CharField(label= 'Apartment_address', widget=forms.TextInput(attrs = {
                'class': 'form-control',
                'style': "width: 700px; background: black; color: white; font-family: 'Noto Serif', serif"
            }))
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={
                'class': 'form-control',
                'value': 'Mumbai',
                'style': "width: 110px;background: black; color: white; font-family: 'Noto Serif', serif;"
            }))
    pincode= forms.IntegerField(label= 'Pin-code', widget=forms.TextInput(attrs={
                'class': 'form-control',
                'style': "width:90px; background: black; color: white; font-family: 'Noto Serif', serif;",
                'value': 400000
            }))

    def clean_city(self):
        data= self.cleaned_data['city']
        if data != 'Mumbai':
            data = 'Mumbai'
            return data
        else:
            return data
    def clean_pincode(self):
        data= self.cleaned_data['pincode']
        data=int(data)
        if data<400000 and data>499999:
            raise ValidationError('Not Mumbai Pin-Code try another one')
        else:
            return data
