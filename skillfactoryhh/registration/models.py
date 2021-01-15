from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name="profile")

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




