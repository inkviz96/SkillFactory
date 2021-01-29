from django.urls import path
from .views import post_to_googlesheet

urlpatterns = [
    path('', post_to_googlesheet)
]
