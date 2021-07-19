from django.db import models
from django.shortcuts import reverse

# AbtractUser:
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.utils import  timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.

# BaseUserManager
class Manager(BaseUserManager):
    def create_superuser(self, email, username, first_name, last_name, password,phone, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned as staff')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned as Superuser')
        return self.create_user(email, username, first_name, last_name,phone, password, **other_fields)

    def create_user(self, email, username, first_name, last_name, phone,password, **other_fields):
        if not email:
            raise ValueError(_('You must provide email'))
        email= self.normalize_email(email)
        user = self.model(email=email, username= username, first_name=first_name,last_name=last_name,phone=phone, **other_fields)
        user.set_password(password)
        user.save()
        return user

# custom django model for users
class NewUser(AbstractBaseUser,PermissionsMixin,):
    class GenderChoices(models.TextChoices):
        Male = 'Male'
        Female = 'Female'
        Others = 'Others'

    email = models.EmailField(_('email address'), unique = True)         # present in default auth.User
    username = models.CharField(max_length=20, unique = True)         # present in default auth.User
    first_name = models.CharField(max_length=20, null = False)           # present in default auth.User
    last_name = models.CharField(max_length=20)                               # present in default auth.User

    # additional fields
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(choices=GenderChoices.choices,max_length=7,null=False)
    profile_picture = models.ImageField( upload_to = 'images/', blank=True,  null=True)
    phone = models.PositiveBigIntegerField(validators=[MaxValueValidator(10000000000),
                                                      MinValueValidator(1111111111)], unique=True)
    date_joined = models.DateTimeField(default=timezone.now)          # present in default auth.User
    is_staff = models.BooleanField(default = False)                             # present in default auth.User
    is_active = models.BooleanField(default = True)                            # present in default auth.User
    is_superuser = models.BooleanField(default = False)                     # present in default auth.User

    def update_user_url(self):
        return reverse('update-profile', kwargs={
            'pk': self.pk
        })
    # link create_user and create_superuser from Manager to our model NewUser
    objects = Manager()

    # USERNAME_FIELD is basically an identifier for the user that is created
    USERNAME_FIELD = 'email'

    # Required fields is basically a field that is required even for a superuser while creating a superuser with createsuperuser command
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone', 'gender', 'date_of_birth']

    def __str__(self):
        return self.username