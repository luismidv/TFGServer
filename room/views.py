from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


import json
my_email = "debanien@gmail.com"

@csrf_exempt
def csrf_token_view(request):
    """Returns CSRF token in a response."""
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_exempt  
def my_api_view(request):
    """Handles login with CSRF token"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            type = data.get("type")

            if type == "Register":
                create_user(username,email,password)
                next_call = "Login function"

            else:
                next_call = "Login function"
            


            result = authenticate_user(email,password)
            return JsonResponse({"message": "User Data received!", "Resultado": result, "Username": username, "Email": email, "Password": password, "Next_call": next_call})
            

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    elif request.method == "GET":
        return JsonResponse({"GET":"Entrando en el TFGServer"})
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def algo_view(request):
    """Handles login with CSRF token"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            work_time = data.get("worktime")
            morn_night = data.get("biorythm")
            studies = data.get("studies")
            read = data.get("read")
            pets = data.get("pets")
            cooking = data.get("cooking")
            sport = data.get("sport")
            smoke = data.get("smoke")
            organized = data.get("organized")

            return JsonResponse({"message": "User Data received!", "work_time" : work_time, "Morn_night" : morn_night})
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
    elif request.method == "GET":
        return JsonResponse({"GET":"Entrando en el TFGServer"})
    

    

def create_user(username, email, password):
    user = User.objects.create_user(username, email, password)

def change_password(user,new_password):
    u = User.objects.get(username=user)
    u.set_password(new_password)
    u.save()

def authenticate_user(user_name,new_pass):
    user = authenticate(username = user_name, password = new_pass)

    return "Login correct" if user is not None else "Login incorrect"

def log_user(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username,password)

    if user is not None:
        login(request,user)
    else:
        print("Login error")

def log_out(request):
    logout(request)
