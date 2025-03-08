from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from MLSystem import resultview as rv
import logging
import requests

logger = logging.getLogger(__name__)


import json
my_email = "debanien@gmail.com"

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email, 
        })

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
                user = create_user(username,email,password)
                if user is not None:
                    connection_bool = authenticate_user(email,password)
                else:
                    return False
            else:
                connection_bool = authenticate_user(email,password)
            
            return JsonResponse({"message": "User Data received!", "Resultado": connection_bool})
            

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    elif request.method == "GET":
        return JsonResponse({"GET":"Entrando en el TFGServer"})
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


@api_view(['POST'])  # Change to GET if needed
@permission_classes([IsAuthenticated])  # Ensures JWT authentication
def algo_view(request):
    
    if request.method == "POST":
        try:
            #GET THE USER FROM THE REQUEST
            user = request.user
            #GET THE TENANT ASSOCIATED WITH THE USER
            user_data = user.id

            if user_data is None:
                tenant_list = "Not found"
                return tenant_list
            
            else:
                url = "https://luismidv-mlsystemtfg.hf.space/predict/"
                params = {"id": str(user_data)}
                response = requests.post(url, params = params)
                if response.status_code == 200:
                    response_data = response.json()
                    return JsonResponse({"message": "User identified!" , "user": response_data})
            
        
        except Exception as e:
            logger.error(f"Error in algo_view {str(e)}")
            return JsonResponse({"error procesing  request view:"}, status=400)
        
    elif request.method == "GET":
        return JsonResponse({"GET":"Entrando en el TFGServer"})
    
def create_user(username, email, password):
    user = User.objects.create_user(username, email, password)
    return user

def change_password(user,new_password):
    u = User.objects.get(username=user)
    u.set_password(new_password)
    u.save()

def authenticate_user(user_name,new_pass):
    user = authenticate(username = user_name, password = new_pass)
    return True if user is not None else False

def log_user(request, username,password):
    user = authenticate(request, username,password)
    
    if user is not None:
        login(request,user)
        return True
    else:
        print("Login error")
        return False

def log_out(request):
    logout(request)

