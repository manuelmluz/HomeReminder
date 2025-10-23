from django import forms
from django.forms import ModelForm
from .models import Reminder, User
from django.contrib.auth.forms import UserCreationForm

# i kinda wanna add the user automatically here in forms
class Add_Reminder_Form(ModelForm):
    reminder_name = forms.CharField(label="Reminder name", max_length=100)
    reminder_description = forms.CharField(label="Reminder Description", max_length=300)
    reminder_start_date = forms.DateField() 
    # this is a time field i think not sure though
    # not what we want ,maybe a date field or like 5 years 2 years 1 year 6 months etc
    reminder_time_between = forms.DurationField()

    class Meta:
        # STILL NEED TO ADD THE USERNAME FOR THE DATABASE
        model = Reminder
        fields = ['reminder_name', 'reminder_description', 'reminder_start_date','reminder_time_between']

class Register(UserCreationForm):
    # how do i make sure username is unique
    """
    username = forms.CharField(label="username",max_length=100)
    email = forms.CharField(label="email",max_length=100)
    password = forms.CharField(label="password", max_length=100)
    """
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")