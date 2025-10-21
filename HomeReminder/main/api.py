import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Reminder

@login_required
def reminders_api(request):
    print("THIS IS BEING CALLED HEHEHEHEHEHEHEHE")
    print(request.user)
    # i think this works mayhaps
    reminders = Reminder.objects.filter(creator_username=request.user)

    # might need to add additional fields 
    data = list(reminders.values(
            "id", "reminder_name", "reminder_description", "reminder_start_date"
        ))
    
    print("THIS IS THE JSON",data)
    return JsonResponse(data, safe=False)
    