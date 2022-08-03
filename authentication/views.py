from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.contrib import messages
from django.contrib import auth

# Create your views here.

class UsernameValidationView(View):
    def post(self, request):
        username = json.loads(request.body)["username"]

        if not username.isalnum():
            return JsonResponse({"username_error": "Username is not a valid"},status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error": "Username is taken"},status=409)
            
        
        return JsonResponse({"username_valid": True})

class EmailValidationView(View):
    def post(self, request):
        email = json.loads(request.body)["email"]

        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error": "Email is taken"},status=409)
        
        return JsonResponse({"email_valid": True})

class RegistirationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        #get user data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        #validate 
        if not User.objects.filter(username=username, email=email).exists():
            if len(password) < 8:
                messages.info(request, "Password is too short")
                return render(request, 'authentication/register.html')
                
            user =User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()
            messages.success(request, "Account successfully created")
            return render(request, 'authentication/register.html')
            
        #create usear


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                messages.success(request, f"Welcome {user.username} now you are logged in!")
                return redirect('expenses')
            else:
                messages.info(request, "Incorrect username or password.")
                return render(request, 'authentication/login.html')
        else:
            messages.info(request, "Please fill all the fields.")
            return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('login')