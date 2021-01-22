from django.urls import include, path

from .views import CompanyProfileListCreateView, CompanyProfileDetailView, RegistrationCompanyAPIView, \
    LoginCompanyAPIView

urlpatterns = [
    path('companies/registration/', RegistrationCompanyAPIView.as_view()),
    path('companies/login/', LoginCompanyAPIView.as_view()),
    # gets all companies profiles and create a new profile
    path("all-companies-profiles", CompanyProfileListCreateView.as_view(), name="all-companies-profiles"),
    # retrieves profile details of the currently logged in user
    path("company-profile/<int:pk>", CompanyProfileDetailView.as_view(), name="company-profile"),
]