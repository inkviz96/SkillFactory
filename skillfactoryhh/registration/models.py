from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from registration_students.models import User
from django.contrib.auth.models import BaseUserManager, PermissionsMixin


class CompanyManager(BaseUserManager):

    def create_company(self, email, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')

        company = Company(
            email=self.normalize_email(email),
        )
        company.set_password(password)
        company.save()

        return company


class Company(User, PermissionsMixin):

    USERNAME_FIELD = 'email'

    objects = CompanyManager()


class CompanyProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                             related_name="profile")

    company_name = models.CharField(blank=False, max_length=30)
    scope = models.CharField(blank=False, max_length=30)
    address = models.CharField(blank=False, max_length=100)
    about_company = models.TextField(blank=True)
    about_team = models.TextField(blank=True)
    contact_person = models.CharField(blank=False, max_length=256)
    position = models.CharField(blank=True, max_length=256)
    email = models.EmailField(blank=False, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name



