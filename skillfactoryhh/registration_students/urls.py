from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import RegistrationAPIView, account_confirmation


urlpatterns = [
    path('api/registration/', RegistrationAPIView.as_view(), name='register'),
    path('api/login/', obtain_auth_token, name='login'),
    path('api/confirm_account/', account_confirmation),
]
