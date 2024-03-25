from django.urls import path
from . import views

urlpatterns = [
    path("", views.LoginPageView.as_view(), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("signup/", views.signup_page, name="signup")
]