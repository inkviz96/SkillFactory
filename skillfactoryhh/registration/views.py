from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView,)
from .models import CompanyProfile
from .permissions import IsOwnerProfileOrReadOnly
from .renderers import UserJSONRenderer
from .serializers import CompanyProfileSerializer, RegistrationCompanySerializer, LoginCompanySerializer
from django.core.mail import EmailMultiAlternatives
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class RegistrationCompanyAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationCompanySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginCompanyAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginCompanySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyProfileListCreateView(ListCreateAPIView):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (JWTAuthentication,)

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_authenticated:
            serializer.save(user=user)
        else:
            serializer.save()

        title = f'Заявка на регистрацию компании - {serializer.data.get("company_name")}'

        if serializer.data.get("about_company"):
            about_c = serializer.data.get("about_company")
        else:
            about_c = '-'

        if serializer.data.get("about_team"):
            about_t = serializer.data.get("about_team")
        else:
            about_t = '-'

        if serializer.data.get("position"):
            position = serializer.data.get("position")
        else:
            position = '-'

        message_data = {
            'scope': serializer.data.get("scope"),
            'address': serializer.data.get("address"),
            'about_c': about_c,
            'about_t': about_t,
            'contact_person': serializer.data.get("contact_person"),
            'position': position,
            'email': serializer.data.get("email"),
            'phone': serializer.data.get("phone_number")
        }

        html_content = render_to_string('email/company_application.html', message_data)
        text_content = strip_tags(html_content)

        message = EmailMultiAlternatives(subject=title, body=text_content, from_email='example_1@gmail.com', to=['example_2@yandex.ru'])
        message.attach_alternative(html_content, "text/html")
        message.send()


class CompanyProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    # permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]
