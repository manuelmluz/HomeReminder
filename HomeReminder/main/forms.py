from django import forms
from django.forms import ModelForm
from .models import Reminder


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