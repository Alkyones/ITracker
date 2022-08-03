from .views import EmailValidationView, RegistirationView,EmailValidationView,UsernameValidationView,LoginView,LogoutView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("register/" , RegistirationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("user-val/", csrf_exempt(UsernameValidationView.as_view()), name="username-validation"),
    path("email-val/", csrf_exempt(EmailValidationView.as_view()), name="email-validation"),
    
    ]