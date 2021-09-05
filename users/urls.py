from allauth.account.views import confirm_email
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from users.views import ProfileView

urlpatterns = [
    path(r"profile/<str:pk>", ProfileView.as_view()),
]
