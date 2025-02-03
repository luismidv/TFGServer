from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import json

my_email = "debanien@gmail.com"

def csrf_token_view(request):
    """Returns CSRF token in a response."""
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_exempt  # Remove this in production, use proper CSRF handling
# Create your views here.
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
            # Simulate authentication logic
            #if email == "test@example.com" and password == "password123":
            #    return JsonResponse({"message": "Login successful"}, status=200)
            #else:
            #    return JsonResponse({"message": "Invalid credentials"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    elif request.method == "GET":
        return JsonResponse({"GET":"Entrando en el TFGServer"})
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

    