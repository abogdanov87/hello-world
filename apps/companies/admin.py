from django.contrib import admin

# Register your models here.
from .models import (
    Company
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company
    fields = [
        'name',
        'short_name',
        'inn',
        'badge',
        'active',
    ]
