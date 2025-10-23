from datetime import timedelta,date
from django.db import IntegrityError
from django.test import TestCase, Client
from .models import Reminder, User 
from .forms import Add_Reminder_Form,Register
from django.urls import reverse

# 1. set up code
# 2. logic to test
# 3. assertions

# only test 1 thing per function

# testing database
class TestModels(TestCase):
    def setUp(self):
        """
        Set up for each test
        """
        self.user = User.objects.create_user(username="harry", password="harry123")

    # test for not null stuff
    def test_model_Reminder(self):
    
        instance_of_reminder = Reminder.objects.create(
            creator_username = self.user,
            reminder_name = "toothbrush",
            reminder_description = "changing toothbrush",
            reminder_start_date = date(2024, 1, 27), # this must be "YYYY-MM-DD" or date(YYYY-MM-DD)
            reminder_time_between = timedelta(days=60) #expects timedelta
        )
        self.assertEqual(str(instance_of_reminder), "toothbrush") # this works on the str method in reminders
        # Type and field sanity checks
        self.assertIsInstance(instance_of_reminder, Reminder)
        self.assertEqual(instance_of_reminder.creator_username, self.user)
        self.assertEqual(instance_of_reminder.reminder_start_date, date(2024, 1, 27))
        self.assertEqual(instance_of_reminder.reminder_time_between, timedelta(days=60))

    def test_model_User(self):
        instance_of_user = User.objects.create_user(
            username="hermione",
            password="hermione123",
            email = "hermione@outlook.com"
        )
        self.assertIsInstance(instance_of_user,User)
        self.assertEqual(instance_of_user.username, "hermione")
        self.assertTrue(instance_of_user.check_password("hermione123"))
        self.assertEqual(instance_of_user.email, "hermione@outlook.com")

    def test_unique_username(self):
        # user database already sets up unique usernames
        # already a harry in set up 
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="harry",
                password="harry123",
                email="harry@outlook.com",
            )
            

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        # get a user and log him in 
        self.user = User.objects.create_user(username="harry", password="harry123")
        self.client.login(username="harry", password="harry123")
        #urls
        self.index_url=reverse("index")
        self.user_view_url = reverse("user")

        #we dont actually send the user
        self.payload = {
            "reminder_name" : "toothbrush",
            "reminder_description" : "changing toothbrush",
            "reminder_start_date": date(2024,1,27), # this must be "YYYY-MM-DD" or date(YYYY-MM-DD)
            "reminder_time_between": timedelta(days = 60)
        }
        # might use this later 
        # invalid because it does not pass a date() object
        self.invalid_payload = {
            "reminder_name" : "toothbrush",
            "reminder_description" : "changing toothbrush",
            "reminder_start_date": "2024-01-27", # this must be "YYYY-MM-DD" or date(YYYY-MM-DD)
        }

    """
    INDEX_VIEW
    """
    
    def test_index_GET(self):
        #mock the response
        response = self.client.get(self.index_url)
        #print(response)
        #assertions:
        # 302 because it redirects to user if its logged in and harry is logged in
        self.assertEqual(response.status_code, 302)

    """
    REGISTER_VIEW
    """  

    """
    LOGIN_VIEW
    """

    """
    USER_VIEW
    """
    def test_user_view_GET(self):
        response = self.client.get(self.user_view_url)

        self.assertEqual(response.status_code, 200)

    def test_user_view_GET_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.user_view_url)
        self.assertEqual(response.status_code, 302)

    #COME BACK TO THIS AFTER TESTING FORMS
    def test_user_view_POST_add_reminder(self):
        response = self.client.post(self.user_view_url, data=self.payload, follow=False)
        # should redirect back to user
        print("this is the response in test",response)
        
        self.assertEqual(response.status_code, 302)
        # should add a reminder
        self.assertEqual(Reminder.objects.count(),1)
        # last reminder should be the one just added
        self.assertEqual(Reminder.objects.last().reminder_name,"toothbrush")

"""
FORMS:
"""
class TestFormsAddReminder(TestCase):
    def setUp(self):

        self.form_data ={
            "reminder_name":"mattress",
            "reminder_description":"changing it",
            "reminder_start_date":date(2024, 1, 27),
            "reminder_time_between": timedelta(days = 60)
        }

        self.form_data_invalid ={
            "reminder_name":"mattress",
            "reminder_description":"changing it",
            "reminder_start_date":"2024, 1, 27",
            "reminder_time_between": "60"
        }
        
    def test_Add_Reminder_Form(self):
        form = Add_Reminder_Form(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_Add_Reminder_Form_invalid(self):
        form = Add_Reminder_Form(data=self.form_data_invalid)
        self.assertFalse(form.is_valid())

class TestFormsRegistering(TestCase):
    def setUp(self):
        self.form_data ={
            "username":"manuelmluz",
            "email":"manuelmendesluz@outlook.com",
            "password1":".0N4zw&_V904",
            "password2":".0N4zw&_V904"
        }
        # this is invalid :)
        self.form_data_invalid ={
            "username":"harry",
            "email":"harry@live.com",
            "password1":"123",
            "password1":"123",           
        }
    def test_registering_form(self):
        # requires 1 more field 
        form = Register(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_registering_form_invalid(self):
        form = Register(data=self.form_data_invalid)
        self.assertFalse(form.is_valid())