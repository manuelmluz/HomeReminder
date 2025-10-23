from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from.models import Reminder
from .forms import Add_Reminder_Form
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
            return HttpResponseRedirect(reverse("user"))
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
        return HttpResponseRedirect(reverse("user"))
    else:
        return render(request, "main/register.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))



@login_required
def user_view(request):
    user = request.user
    reminders = user.reminders.all().order_by("reminder_start_date")

    if request.method == "POST":
        form = Add_Reminder_Form(request.POST, request.FILES)
        if form.is_valid():
            #could add a try and except here so it can handle error better
            obj = form.save(commit=False)
            obj.creator_username = user
            obj.save()
            
            return redirect("user")  # /me/
    else:
        form = Add_Reminder_Form()

    return render(request, "main/user_page.html", {
        "user": user,
        "reminders": reminders,
        "form": form,   # pass the *instance*, not the class
    })

    #return render(request, "main/user_page.html")