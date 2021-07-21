from django import forms
from.models import *

class CheckoutForm(forms.Form):
    street_name = forms.CharField(label='Street name', max_length=20, widget=forms.TextInput(attrs={
                "class": 'form-control',
                "placeholder": 'Street name',
                "style": "width: 600px;"
            }))
    apartment_address = forms.CharField(label= 'Apartment address', widget=forms.Textarea(attrs = {
                'class': 'form-control',
                'style': "width: 600px; height: 100px;",
                'cols': '20',
                'rows': '5'
            }))
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={
                'class': 'form-control-plaintext',
                'value': 'Mumbai',
                'style': "width: 150px;",
                'readonly': True
            }))
    pincode = forms.IntegerField(label= 'Pin-code', widget=forms.TextInput(attrs={
                'class': 'form-control',
                'value': 400000
            }))

    def clean_city(self):
        city = self.cleaned_data['city']
        if city != 'Mumbai':
            raise ValidationError("* City should be Mumbai")
        return city

    def clean_pincode(self):
        pincode = self.cleaned_data['pincode']
        pincode = int(pincode)
        if (pincode < 400000) or (pincode > 499999):
            raise ValidationError("* Not Mumbai Pin-Code try another one")
        return str(pincode)

    def clean_apartment_address(self):
        apt_add = self.cleaned_data['apartment_address'].lower()
        for i in apt_add:
            if len(apt_add) < 20 or len(apt_add) > 150:
                raise ValidationError("* length of address should be 20-150.")
            if (ord(i) > 122 or ord(i) < 97) or (ord(i) not in [44, 45, 46, 47]) or (ord(i) < 48 or ord(i) > 57):
                raise ValidationError("* Enter letters and ', . / -' only.")
        return apt_add

    def clean_street_name(self):
        st_name= self.cleaned_data['street_name'].lower()
        for i in st_name:
            if (ord(i) > 122 or ord(i) < 97) or (ord(i) < 48 or ord(i) > 57):
                raise ValidationError("* Enter letters and numbers only.")
        return st_name.capitalize()