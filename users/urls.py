from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/github/", views.github_login, name="github-login"),
    path("login/github/callback/", views.github_callback, name="github-callback"),
    path("logout/", views.LogOutView.as_view(), name="logout"),
    path("sigup/", views.SignUpView.as_view(), name="signup"),
    path("verify/<str:key>", views.complete_verification, name="verification"),
    path("verify/<str:key>", views.complete_verification, name="verification"),
    path("profile/<int:pk>", views.UserProfileView.as_view(), name="profile"),
    path("update-profile/", views.UserProfileUpdate.as_view(), name="update"),
    path("update-password/", views.UpdatePassword.as_view(), name="password"),
    path("start-hosting/", views.switch_hosting, name="switch-hosting"),
]
