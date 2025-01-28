from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def my_api_view(request):
    if request.method == 'POST':
        data = request.POST.get('data', 'No data provided')
        return JsonResponse({'message': 'Data received', 'data': data})
    
    return JsonResponse({'error': 'Invalid request'}, status = 400)