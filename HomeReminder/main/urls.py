from django.urls import path

from . import views, api

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("u/<str:username>", views.user_view, name="user"),

    # apis
    path("api/reminders", api.reminders_api, name="reminders-api")
]
