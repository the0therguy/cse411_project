from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from .models import *

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('B', 'Bkash'),
    ('C', 'Cash')
)


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class CheckoutForm(forms.Form):
    street_address = forms.CharField(required=False)
    apartment_address = forms.CharField()
    phone_number = forms.CharField()
    area_address = forms.CharField()
    district = forms.CharField()
    payment_options = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
