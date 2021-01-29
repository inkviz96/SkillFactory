from django.shortcuts import HttpResponse, get_object_or_404, reverse
from django.contrib.auth.models import User
from rest_framework.response import Response
from password_manage.serializers import RestoreAccessSerializer, \
    ChangePasswordSerializer
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from skillfactoryhh.settings import EMAIL_HOST_USER
from django.core.exceptions import ValidationError


@api_view(['POST'])
def restore_access(request):
    serializer = RestoreAccessSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    user = get_object_or_404(User, email=email)
    link = request.build_absolute_uri(reverse(change_password, args=[user.pk]))
    send_mail('Password changing', link, EMAIL_HOST_USER,
              [user.email], fail_silently=False)

    return Response({'email_send': True})


@api_view(['POST'])
def change_password(request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if serializer.validated_data['password'] == serializer.validated_data[
        'confirm_password']:
        user.set_password(serializer.validated_data['password'])
        user.save()
    else:
        raise ValidationError('Passwords do not match')
    return Response({'password': 'saved'})
