from django.urls import path

from .views import RegistrationAPIView, LoginAPIView


urlpatterns = [
    path('api/registration/', RegistrationAPIView.as_view(), name='registration'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
]
