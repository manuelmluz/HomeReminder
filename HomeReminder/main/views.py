from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from.models import Reminder
#from .forms import listing_form 

from .models import User

# Create your views here.

def index(request):
    # if user is authenticated get his reminders
    if request.user.is_authenticated: # need to fix this
        pass
    else:
        return HttpResponseRedirect(reverse("login"))

    return render(request, "main/index.html",{
        
    })


def login_view(request):

    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            #login user and send him to user_page, need to send him the user name
            return HttpResponseRedirect(reverse("user", args=(username,)))
        else:
            return render(request, "main/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "main/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "main/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "main/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("user", args=(username,)))
    else:
        return render(request, "main/register.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def user_view(request, username):
    # we might need to authenticate it like in login_view
    
    #print(username)

    # any user logged in is authenticated i think
    if request.user.is_authenticated: # do we need to authenticate the user again
        #gets the username
        user = get_object_or_404(User, username=username)
        #gets the usernames reminders as a list
        reminders = user.reminders.all().order_by("reminder_start_date")  
        print(user)
        print(reminders)
        # reminders object is now passed down
        return render(request,"main/user_page.html",{
            "user":user,
            "reminders":reminders
        })
        
    else:
        print("user is NOT authenticated")
        return HttpResponseRedirect(reverse("login"))

    #return render(request, "main/user_page.html")