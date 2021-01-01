from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from registration.models import CompanyProfile
from django.contrib.auth.models import User
from .views import CompanyProfileListCreateView
from .serializers import CompanyProfileSerializer
from django.core import mail
from skillfactoryhh.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

import json


class RegistrationCompanyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('SkillfactoryAdmin', password='SkillfactoryAdmin')
        CompanyProfile.objects.create(user=user, company_name='Skillfactory',
                                      scope='Education', address='MSK',
                                      about_company='It online school', about_team='Company SF',
                                      email='example@example.com', phone_number='+70000000000',
                                      confirmation='False')

    def test_user_label(self):
        company_prof = CompanyProfile.objects.get(id=1)
        field_label = company_prof._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_company_name_label(self):
        company_prof = CompanyProfile.objects.get(id=1)
        field_label = company_prof._meta.get_field('company_name').verbose_name
        self.assertEquals(field_label, 'company name')

    def test_company_name_max_length(self):
        company_prof = CompanyProfile.objects.get(id=1)
        max_length = company_prof._meta.get_field('company_name').max_length
        self.assertEquals(max_length, 30)

    def test_scope_label(self):
        company_prof = CompanyProfile.objects.get(id=1)
        field_label = company_prof._meta.get_field('scope').verbose_name
        self.assertEquals(field_label, 'scope')

    def test_scope_max_length(self):
        company_prof = CompanyProfile.objects.get(id=1)
        max_length = company_prof._meta.get_field('scope').max_length
        self.assertEquals(max_length, 30)

    def test_address_label(self):
        company_prof = CompanyProfile.objects.get(id=1)
        field_label = company_prof._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'address')

    def test_address_max_length(self):
        company_prof = CompanyProfile.objects.get(id=1)
        max_length = company_prof._meta.get_field('address').max_length
        self.assertEquals(max_length, 100)

    def test_about_company_label(self):
        company_prof = CompanyProfile.objects.get(id=1)
        field_label = company_prof._meta.get_field('about_company').verbose_name
        self.assertEquals(field_label, 'about company')

    def test_about_team_label(self):
        company_prof = CompanyProfile.objects.get(id=1)
        field_label = company_prof._meta.get_field('about_team').verbose_name
        self.assertEquals(field_label, 'about team')

    def test_email_label(self):
        company_prof = CompanyProfile.objects.get(id=1)
        field_label = company_prof._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'email')

    def test_phone_number_label(self):
        company_prof = CompanyProfile.objects.get(id=1)
        field_label = company_prof._meta.get_field('phone_number').verbose_name
        self.assertEquals(field_label, 'phone number')

    def test_confirmation_label(self):
        company_prof = CompanyProfile.objects.get(id=1)
        field_label = company_prof._meta.get_field('confirmation').verbose_name
        self.assertEquals(field_label, 'confirmation')


class APITests(APITestCase):
    def test_api_response_company(self):
        url = reverse('all-companies-profiles')
        data = {
            "user": "user",
            "company_name": "name",
            "scope": "IT",
            "address": "MSK",
            "about_company": "about",
            "about_team": "about",
            "email": "example@exakjle.com",
            "phone_number": "+79819913306",
            "confirmation": "false"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CompanyProfile.objects.count(), 1)
        self.assertEqual(CompanyProfile.objects.get().id, 1)

        factory = APIRequestFactory()
        view = CompanyProfileListCreateView.as_view()
        request = factory.get("company-profile/1")
        response = view(request, pk='1')
        response.render()
        get_data = {'id': 1,
                    'user': None,
                    'company_name': 'name',
                    'scope': "IT",
                    'address': "MSK",
                    'about_company': "about",
                    'about_team': "about",
                    'email': "example@exakjle.com",
                    'phone_number': "+79819913306",
                    'confirmation': False
                    }
        self.assertEqual(json.loads(response.content)[0], get_data)


class EmailTest(TestCase):
    def test_send_email(self):
        # Send message.
        mail.send_mail(
            'Subject here', 'Here is the message.',
            EMAIL_HOST_USER, [EMAIL_HOST_USER],
            fail_silently=False,
        )
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Subject here')
