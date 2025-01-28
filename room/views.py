from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token


# Create your views here.
def my_api_view(request):
    if request.method == 'POST':

        csrf_token = request.COOKIES.get('csrftoken', None)
        if csrf_token is None:
            return JsonResponse({'error': 'CSRF token not found'}, status=403)
        
        
        data = request.POST.get('data', 'No data provided')
        return JsonResponse({'message': 'Data received', 'data': data, 'csrf_token': csrf_token})
    
    csrf_token = get_token(request)
    response = JsonResponse({'message': 'CSRF token set in cookie'})
    
    # Set the CSRF token in the cookie
    response.set_cookie('csrftoken', csrf_token, httponly=False, samesite='None', secure=True)  # Use secure=True in production

    return response