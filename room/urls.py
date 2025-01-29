from django.urls import path
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import views
app_name = 'room'

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path('api/my_endpoint/', views.my_api_view, name='my_api_view'),
    path("csrf/", csrf_token_view),  # Fetch CSRF token

]
