from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path to djoser end points
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # path to registration's app endpoints
    path("api/registration/", include("registration.urls")),
    path('', include('registration_students.urls')),
    path('api/google/', include('googlesheets.urls')),
    path('', include('password_manage.urls')),
]
