from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class SignupForm(UserCreationForm):
    mobile_num_regex = RegexValidator(regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!")
    phone_number = forms.CharField(validators=[mobile_num_regex])
    choices = (
        ('male', "Male"),
        ("female", "Female")
    )
    sex = forms.ChoiceField(choices=choices)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {'phone_number': 'phone_number', 'sex': 'sex'}
