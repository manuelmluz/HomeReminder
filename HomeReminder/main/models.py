
from django.contrib.auth.models import AbstractUser
from django.db import models

# for single user create model instance methods
# for set-based queries use a custom query set/ manager

# Create your models here.
#does this class already have string representation??
class User(AbstractUser):
    # this already enforces unique username
    # abstract user already has name password username type shit
    # can still add more if needed
    
    #listings field??
    
    pass

class Reminder(models.Model):

    # link the user_id with his reminders, when calling Reminders now you can access all of the User table Reminder.creator_id.user_id
    creator_username = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "reminders")
 
    reminder_name = models.CharField(max_length=100)
    reminder_description = models.TextField(max_length= 500, blank=True)
    # we'll set it now that its empty 
    reminder_start_date = models.DateField() 
    # this is a time field i think not sure though
    # not what we want ,maybe a date field or like 5 years 2 years 1 year 6 months etc

    reminder_time_between = models.DurationField()

    """
    to set the right duration!!!
    my_model = MyModel()
    my_model.duration = datetime.timedelta(days=20, hours=10)   

    only goes up to days, so will need to change it in the form to match the database
    """

    def __str__(self):
        return self.reminder_name

