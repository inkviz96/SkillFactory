from django.urls import path
from password_manage import views

urlpatterns = [
    path('restore_access/', views.restore_access,
         name='restore_access'),
    path('change_password/<int:pk>/', views.change_password,
         name='change_password'),
]