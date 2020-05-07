from django.contrib import admin
from .models import (
    Param,
)

class ParamInline(admin.TabularInline):
    model = Param
    fields = ('code', 'name', 'value_type', 'value', 'active')
    extra = 0