from django.urls import path

from .views import RegistrationAPIView


urlpatterns = [
    path('api/registration/', RegistrationAPIView.as_view(), name='registration'),
]
