from django.contrib import admin
from .models import CompanyProfile, Company


@admin.register(CompanyProfile)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Company)
class AuthorAdmin(admin.ModelAdmin):
    pass


