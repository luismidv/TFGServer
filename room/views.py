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
            user_data = user.id
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
            response = logged_algo_view(user_data)
            return JsonResponse(response)
        
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
                    INSERT INTO rooms (id, direction, city, state, rooms, bathrooms, metters, price, description, lessor_id) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, [new_id,
                        data["direction"], data["city"], data["state"],
                        data["rooms"], data["bathrooms"], data["metters"],
                        data["price"], data["description"], data["lessorId"]
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
                result = log_lessor(data["username"], data["password"])
                if result[1]:
                    return JsonResponse({"message" : "Register correct", "lessor_data" : result[0], "username": data["username"]})
                else:
                    return JsonResponse({"message" : "Login failed"})
            
        elif type == "Login":
            with connection.cursor() as cursor:
                username = data["username"]
                password = data["password"]
                id,log_bool = log_lessor(username,password)
                if log_bool:
                    lessor_information = get_rooms(username)
                    if len(lessor_information) != 0:
                        return JsonResponse({"message" : "Login correct", "rooms_data" : lessor_information, "lessor_data" : id})
                    else:
                        cursor.execute("""
                        SELECT id
                        FROM auth_lessor 
                        WHERE auth_lessor.username = %s
                        """, [username])
                        result = cursor.fetchone()
                        return JsonResponse({"message" : "Login correct", "rooms_data" : lessor_information, "lessor_data" : result[0]})

                else:
                    return JsonResponse({"message" : "Login incorrect", "password" : lessor_information, "introduced_password" : log_bool})
        
        elif type == "Refresh":
            with connection.cursor() as cursor:
                username = data["username"]
                cursor.execute("""
                        SELECT id
                        FROM auth_lessor 
                        WHERE auth_lessor.username = %s
                        """, [username])
                result = cursor.fetchone()
                lessor_information = get_rooms(username)
                if len(lessor_information) != 0:
                    return JsonResponse({"message" : "Data refreshed != 0", "rooms_data" : lessor_information, "lessor_data" : result[0]})
                else:
                    return JsonResponse({"message" : "Data refreshed != 0", "rooms_data" : lessor_information, "username" : username , "lessor_data" : result[0]})
                
        
@csrf_exempt                
def log_lessor(username, password):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id,password FROM auth_lessor WHERE username =" + "'"+ username + "'")
        result = cursor.fetchone()
        if result is not None:
            pass_bool = check_password(password, result[1])
            return_list = [result[0], pass_bool]
            return return_list
        else:
            return pass_bool
            
@csrf_exempt
def get_rooms(username):
    with connection.cursor() as cursor:
        try:
            cursor.execute("""
                SELECT rooms.*, auth_lessor.username, auth_lessor.id AS lessor_id
                FROM auth_lessor 
                JOIN rooms ON auth_lessor.id = rooms.lessor_id 
                WHERE auth_lessor.username = %s
            """, [username])
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return result
        except Exception as e:
            print(f"Error while trying to get user rooms:  {e}")

@csrf_exempt
def room_mod(request):
    if request.method == "POST":
        data = json.loads(request.body)
        type = data["action"]
        room_id = data["room_id"]

        if type == "modification":
            print("Modification actions")
        
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                    DELETE FROM rooms WHERE id = %s
                """, [room_id])
                return JsonResponse({"message": f"Room deleted successfully"})
            except Exception as error:
                return JsonResponse({"message" : f"Error at deleting room {error}"})
                

def logged_algo_view(user_data):
    try:
        url = "https://luismidv-mlsystemtfg.hf.space/predict/"
        params = {"id": str(user_data)}
        response = requests.post(url, params = params)
        if response.status_code == 200:
            response_data = response.json()
            return response_data
    except Exception as e:
        print(f"Exception ocurred {e}")
        
    

def change_password(user,new_password):
    u = User.objects.get(username=user)
    u.set_password(new_password)
    u.save()



