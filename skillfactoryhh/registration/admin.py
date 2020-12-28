from django.contrib import admin
from .models import CompanyProfile


@admin.register(CompanyProfile)
class AuthorAdmin(admin.ModelAdmin):
    pass


