from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm  # default django form
from django.contrib.auth.models import User # default django user model
from django.core.exceptions import ValidationError
from django.core.validators import *
from datetime import date, datetime
# from django.core.exceptions.Multiple import
from .models import NewUser
from django.forms.widgets import *
# from .models import User
from django.contrib.auth.forms import AuthenticationForm

# custom django form
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Username', min_length=10, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Sachin100', 'style': 'width: auto', 'class': 'form-control'}),  required = True)
    email = forms.EmailField(label='Email',required=True, widget=forms.EmailInput(attrs={'placeholder': 'Sachin100x100@legends.com', 'style': 'width: 500px;', 'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', min_length=3, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Sachin', 'style': 'width: auto;', 'class': 'form-control'}),  required = True)
    last_name = forms.CharField(label='Last Name', min_length=3, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Tendulkar', 'style': 'width: auto;', 'class': 'form-control'}),  required = True)
    profile_picture = forms.ImageField(required=False)
    gender_choices = (('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others'))
    gender = forms.ChoiceField(choices = gender_choices, widget = forms.Select(attrs={'class': 'form-control', 'style': ' width: 100px;'}), required=True)
    phone = forms.IntegerField(label = 'Phone no.', min_value=1111111111, max_value=9999999999, widget=forms.NumberInput(attrs={'placeholder': '9999999999', 'style': 'width: auto;', 'class': 'form-control'}), required=True)
    date_of_birth = forms.DateField(label="Date of Birth", required=True, widget=forms.DateInput(format=['%d/%m/%y'], attrs={'placeholder': 'dd/mm/yyyy', 'style': 'width: 245px;', 'type': 'date', 'class': 'form-control', 'max': '2000-01-01', 'min': '1950-01-01'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={ 'class': 'form-control', 'style': 'width: auto', 'maxlength': '20', 'minlength': '10'}), required=True)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={ 'class': 'form-control', 'style': 'width: auto'}), required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        un = NewUser.objects.filter(username=username)
        if un.count():
            raise ValidationError("* Username taken. Try another one")
        return username
    def clean_email(self):
        email = self.cleaned_data['email']
        em = NewUser.objects.filter(email=email)
        if em.count():
            raise ValidationError('* Email taken. Try another one')
        return email
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2 and len(password1) < 20 and len(password2) < 20 and len(password1) > 10 and len(password2) > 10:
            raise ValidationError("* Password don't match. Make sure you entered same password in both fields")
        return password2

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        return date_of_birth


    class Meta:
        model = NewUser
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_picture', 'gender', 'phone', 'date_of_birth',
                  'password1', 'password2', ]

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=True)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.profile_picture = self.cleaned_data['profile_picture']
        user.gender = self.cleaned_data['gender']
        user.phone = self.cleaned_data['phone']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        if commit:
            user.save()
        return user

class Customlogin(AuthenticationForm):
    class Meta:
        model = NewUser
        fields= ['email', 'password']
        widget={
            'email': EmailInput(attrs={'class': 'form-control', 'style': 'width: 100%'}),
            'password': PasswordInput(attrs={'class': 'form-control'})
        }

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        em = NewUser.objects.filter(email = email)
        if em.count() == True:
            raise ValidationError('* Email is not registered. Try logging in with registered Email id.')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        return password

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = {
             'email',  'first_name', 'last_name', 'profile_picture', 'gender', 'phone'
        }
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control', 'type': 'email'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'style': 'width: 170px;'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'style': 'width: 170px;'}),
            'profile_picture': ClearableFileInput(attrs={'class': 'custom-file-input', }),
            'gender': Select(attrs={'class': 'form-control', 'style': 'width: 100px;'}),
            'phone': TextInput(attrs={'class': 'form-control', 'style': 'width: 170px;', 'minlength': '10', 'maxlength': '10'})
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone < 1111111111 or phone > 9999999999:
            raise ValidationError('Length of Number should be 10.')
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()

    def clean_first_name(self):
        firstname = self.cleaned_data['first_name'].lower()
        for i in range(len(firstname)):
            if ord(firstname[i]) > 122 or ord(firstname[i]) < 97:
                raise ValidationError("Enter letters only.")
        return firstname.capitalize()

    def clean_last_name(self):
        lastname = self.cleaned_data['last_name'].lower()
        for i in range(len(lastname)):
            if ord(lastname[i]) > 122 or ord(lastname[i]) < 97:
                raise ValidationError("Enter letters only.")
        return lastname.capitalize()

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=20, label= 'Old Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'minlength': '8', 'maxlength': '20'}))
    new_password1 = forms.CharField(max_length=20, label= 'New Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'minlength': '8', 'maxlength': '20'}))
    new_password2 = forms.CharField(max_length=20, label= 'Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'minlength': '8', 'maxlength': '20'}))
    class Meta:
        model = NewUser
        fields = ('old_password', 'new_password1', 'new_password2')

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError("* Incorrect Password.")
        return old_password

    def clean_new_password1(self):
        newp1= self.cleaned_data['new_password1']
        if len(newp1)<8 or len(newp1)>20:
            raise ValidationError("* Enter password with 8-20 characters.")
        else:
            return newp1

    def clean_new_password2(self):
        newp1 = self.cleaned_data.get('new_password1')
        newp2 = self.cleaned_data.get('new_password2')
        if newp1!=newp2:
            raise ValidationError("* Password doesn't match with New Password.")
        else:
            return newp2
