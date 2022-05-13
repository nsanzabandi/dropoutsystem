from dataclasses import field
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from base.models import Student


class userForm(UserCreationForm):
    class Meta:
        model=Student
        fields='__all__'

    USERNAME_FIELD='email'
    
class studentForm(UserCreationForm):
    class Meta:
        model=Student
        fields='__all__'