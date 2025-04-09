from django.urls import path,include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



app_name = 'room'

urlpatterns = [
    # path('', TemplateView.as_view(template_name="index.html")),
    path('api/my_endpoint/', views.my_api_view, name='my_api_view'),
    path("csrf/", views.csrf_token_view),  # Fetch CSRF token
    path('api/algorithm/', views.algo_view, name="algo_view"),
    path('accounts/' , include('django.contrib.auth.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', views.UserView.as_view(), name='user_view'),
    path('api/algo_view/', views.algo_view, name='algo_view'),
    path('api/tenants_features/', views.tenant_features, name="tenant_features"),
    path('api/lessor_room/', views.lessor_room, name="lessor_room"),
    path('api/lessor_identificaiton/', views.lessor_identification, name="lessor_identification"),
    path('api/room_mod/', views.room_mod, name="room_mod")
]
