# awd_main/forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegistrationForm(UserCreationForm):
    # It's good practice to make email required for SaaS apps
    email = forms.EmailField(required=True) 

    class Meta:
        model = User
        fields = ('username', 'email')
        # Django automatically handles password and password confirmation!