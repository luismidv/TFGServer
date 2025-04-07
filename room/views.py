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
from django.db import IntegrityError
from django.db import connection
from django.contrib.auth.hashers import make_password, check_password





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
            with connection.cursor() as cursor:
                cursor.execute("SELECT MAX(CAST(id AS INTEGER)) FROM tenants")
                result = cursor.fetchone()
                if result is not None:
                    new_id = int(result[0])
                    new_id +=1
                    new_id = str(new_id)
                else:
                    return 0
                cursor.execute("""
                    INSERT INTO tenants (id, names, surnames, age, email, worktimes, schedules, "studieslevel", pets, cooking, sport, smoking, organized) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)
                    """,[new_id,
                        data["names"], data["surnames"], data["age"],
                        data["email"], data["worktime"], data["biorythm"],
                        data["studies"],data["pets"],data["cook"], 
                        data["sport"], data["smoke"], data["organized"]
                    ])
            return JsonResponse({"message": "tenant created"}, status=status.HTTP_200_OK)
        
        except Exception as error:
            return JsonResponse({"message": str(error)}, status = status.HTTP_400_BAD_REQUEST)
        
@csrf_exempt 
def lessor_room(request):
    print("Entering lessor room api")
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received data:", data)
            with connection.cursor() as cursor:
                cursor.execute("SELECT MAX(CAST(id AS INTEGER)) FROM rooms")
                result = cursor.fetchone()
                if result is not None:
                    new_id = int(result[0])
                    new_id +=1
                    new_id = str(new_id)
                else:
                    return 0
                cursor.execute("""
                    INSERT INTO rooms (id, direction, city, state, rooms, bathrooms, metters, price, description) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, [new_id,
                        data["direction"], data["city"], data["state"],
                        data["rooms"], data["bathrooms"], data["metters"],
                        data["price"], data["description"]
                    ])

            return JsonResponse({"message": data, "direction": data["direction"], "city": data["city"]}, status=status.HTTP_200_OK)
        
        except IntegrityError as e:
            return JsonResponse({"error": "Database Integrity Error", "details": str(e)}, status=400)

        except Exception as error:
            return JsonResponse({"message": str(error)}, status = status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def lessor_identification(request):
    if request.method == "POST":
        data = json.loads(request.body)
        type = data["type"]
        
        if type == "Register":
            with connection.cursor() as cursor:
                cursor.execute("SELECT MAX(CAST(id AS INTEGER)) FROM auth_lessor")
                result = cursor.fetchone()
                if result is not None:
                    new_id = int(result[0])
                    new_id +=1
                    new_id = str(new_id)
                else:
                    new_id = str(0)
                
                new_password = make_password(data["password"])
                cursor.execute("""
                    INSERT INTO auth_lessor (id, username, email, telephone, password) 
                    VALUES (%s, %s, %s, %s, %s)
                    """, [new_id,
                        data["username"], data["email"], data["telephone"], new_password
                    ])
                log_lessor(data["username"], data["password"])

            return JsonResponse ({"message" : "User registered correctly"})
            
        else:
            with connection.cursor() as cursor:
                username = data["username"]
                password = data["password"]
                cursor.execute("SELECT * FROM auth_lessor WHERE username = " + "'"+ username + "'")
                result = cursor.fetchone()
                if result is None:
                    return JsonResponse({"message":"There is no user for the introduced credential in our database"})
                password_check = check_password(password, result[4])
                if password_check == True:
                    get_rooms(username)
                    return JsonResponse({"message" : "Login correct", "lessor_id" : result[0]})
                
                else:
                    return JsonResponse({"message": "Login incorrect", "success": False})
                
def log_lessor(username, password):
    with connection.cursor() as cursor:
        cursor.execute("SELECT password FROM auth_lessor WHERE username = " + "'"+ username + "'")
        result = cursor.fetchone()
        if result is not None:
            password_check = check_password(password, result[4])
            if password_check == True:
                    return JsonResponse({"message" : "Login correct", "success" : True})

def get_rooms(username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM ")

def change_password(user,new_password):
    u = User.objects.get(username=user)
    u.set_password(new_password)
    u.save()



