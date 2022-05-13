from dataclasses import fields
import email
from enum import unique
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from base .models import *

class createrUser(UserCreationForm):
    username=forms.CharField()
    email= forms.EmailField()
    first_name= forms.CharField(max_length=30)
    last_name= forms.CharField(max_length=30)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        model= User
        fields= ['first_name', 'last_name','email', 'username', 'password1', 'password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already exists")
        return data

class DateInput(forms.DateInput):
    input_type = 'date'

class registerStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields= '__all__'
        
        #  ['Full_name', 'Gender', 
        #  'phone_number', 'levelofEducation', 'reason'] 
        widgets = {
            'DoB': DateInput(),
        }

class sectorForm(forms.ModelForm):
    class Meta:
        model=Sector
        fields='__all__'

class messageForm(forms.ModelForm) :
    class Meta:
        model= Messages
        fields = '__all__'   


