from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import json


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
            email = data.get("email")
            password = data.get("password")
            

            print(f"Received email {email} {password}")

            if my_email == email:
                respuesta = "email correcto"
            
            return JsonResponse({"message": "Data received!", "email": email, "password": password, "respuesta" : respuesta})
            

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
            work_time = data.get("work_time")
            morn_night = data.get("morn_night")
            studies = data.get("studies")
            read = data.get("read")
            pets = data.get("pets")
            cooking = data.get("cooking")
            sport = data.get("sport")
            smoke = data.get("smoke")
            organized = data.get("organized")
            
            return JsonResponse({"message": "Data received!", "email": email, "password": password, "respuesta" : respuesta})
            

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    elif request.method == "GET":
        return JsonResponse({"GET":"Entrando en el TFGServer"})
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


    