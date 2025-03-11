from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from MLSystem import resultview as rv
import logging
import requests
from django.conf import settings
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Tenants, Rooms
from rest_framework_simplejwt.authentication import JWTAuthentication
import json



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
                    tokens,user_data = authenticate_user(username,password)
                    if tokens:
                        return JsonResponse({"message" : "User registered procceed to logg in", "tokens": tokens, "user": user_data })
                else:
                    return False
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

def authenticate_user(username,new_pass):
    tokens = requests.post(f"https://tfgserver.onrender.com/api/token/", data={"username": username, "password": new_pass})
    tokens = tokens.json()
    user = requests.get(f"https://tfgserver.onrender.com/api/user/", headers={"Authorization": f"Bearer {tokens['access']}"})
    if user.status_code == 200:
        user = user.json()
        return tokens,user
    else:
        return None, None
    

def create_user(username, email, password):
    user = User.objects.create_user(username, email, password)
    return user

@api_view(['POST'])  # Change to GET if needed
@permission_classes([IsAuthenticated])  # Ensures JWT authentication
def algo_view(request):
    
    if request.method == "POST":
        try:
            #GET THE USER FROM THE REQUEST
            user = request.user
            #GET THE TENANT ASSOCIATED WITH THE USER
            user_data = user.id
            
            url = "https://luismidv-mlsystemtfg.hf.space/predict/"
            params = {"id": str(user_data)}
            response = requests.post(url, params = params)
            if response.status_code == 200:
                response_data = response.json()
                return JsonResponse(response_data)
            else:
                return JsonResponse({"Error" : "External API error", "details": response.text})
        except Exception as e:
            logger.error(f"Error in algo_view {str(e)}")
            return JsonResponse({"error procesing  request view:"}, status=400)
        
    elif request.method == "GET":
        return JsonResponse({"GET":"Entrando en el TFGServer"})

@api_view(['POST'])  # Change to GET if needed
@permission_classes([IsAuthenticated])  # Ensures JWT authentication
def tenant_features(request):
    print("Entering tenant features")
    if request.method == "POST":
        try:
            user = request.user
            data = json.loads(request.body)
            tenants = Tenants.objects.create(

                names = data.get("names"),
                surnames = data.get("surnames"),
                age = data.get("age"),
                email = data.get("email"),
                worktimes=data.get('worktime'),
                schedules=data.get('biorythm'),
                studies_level=data.get('studies'),
                read=data.get('read'),
                pets=data.get('pets'),
                cookies=data.get('cook'),
                sport=data.get('sport'),
                smoking=data.get('smoke'),
                organized=data.get('organized'),
            )
            return JsonResponse({"message": "Data recevied succesfully"}, status=status.HTTP_200_OK)
        
        except Exception as error:
            return JsonResponse({"message": str(error)}, status = status.HTTP_400_BAD_REQUEST)
        
@csrf_exempt 
def lessor_room(request):
    print("Entering lessor room api")
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            if data != None:
            # room = Rooms.objects.create(

            #     direction = data.get("direction"),
            #     city = data.get("city"),
            #     state = data.get("state"),
            #     rooms = data.get("rooms"),
            #     bathrooms=data.get('bathrooms'),
            #     metters=data.get('metters'),
            #     price=data.get('price'),
            #     description=data.get('description'),
            # )
                return JsonResponse({"message": "Data recevied succesfully"}, status=status.HTTP_200_OK)
        
        except Exception as error:
            return JsonResponse({"message": str(error)}, status = status.HTTP_400_BAD_REQUEST)




def change_password(user,new_password):
    u = User.objects.get(username=user)
    u.set_password(new_password)
    u.save()



