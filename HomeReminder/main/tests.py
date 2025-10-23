from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from datetime import date, timedelta

from .models import Reminder

User = get_user_model()




    

        
