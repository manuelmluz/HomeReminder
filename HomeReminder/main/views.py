from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from .models import Reminder
from .forms import Add_Reminder_Form, Register
#from .forms import listing_form 

from .models import User

# Create your views here.

def index(request):
    # pretty sure its not just authenticated?
    if request.user.is_authenticated: 
        return HttpResponseRedirect(reverse("user"))
    else:
        return HttpResponseRedirect(reverse("login"))
    # this is basically defunct 



def login_view(request):
    login_form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and login_form.is_valid():
        user = login_form.get_user()
        login(request, user)
        # respect ?next=/... if present
        nxt = request.GET.get("next")
        if nxt:
            return redirect(nxt)
        return redirect("user")
    return render(request, "main/login.html", {
        "login_form": login_form})

def register(request):

    if request.method == "POST":
        register_form = Register(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            #login(request, user) dont log them in
            return redirect("login")
        #what if the form is not valid???
    else:
        register_form = Register()
    #print("THIS IS THE FORM",register_form)
    return render(request, "main/register.html",{
        "register_form": register_form,
    })

    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))



@login_required
def user_view(request):
    user = request.user
    reminders = user.reminders.all().order_by("reminder_start_date") #need to pass it down to html

    if request.method == "POST":
        # can probably just make this whole post thing into a function

        #dont know what request.files does or even if its needed lmao
        form = Add_Reminder_Form(request.POST, request.FILES)
        #print("this is what we get", request.POST, "idk what this is :", request.FILES)
        if form.is_valid():
            #could add a try and except here so it can handle error better
            obj = form.save(commit=False)
            # this adds the creator username, MIGHT MOVE THIS TO FORMS
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