from django.urls import path,include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import views


app_name = 'room'

urlpatterns = [
    # path('', TemplateView.as_view(template_name="index.html")),
    path('api/my_endpoint/', views.my_api_view, name='my_api_view'),
    path("csrf/", views.csrf_token_view),  # Fetch CSRF token
    path('api/algorithm/', views.algo_view, name="algo_view"),
    path('accounts/' , include('django.contrib.auth.urls'))    


]
