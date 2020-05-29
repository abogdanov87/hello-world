from django.contrib import admin

# Register your models here.
from .models import (
    Report,
)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    model = Report
    fields = (
        'name',
        'company',
        'document_template',
        'content_type',
        'active',
    )
    list_display = ('name',)
    list_display_links = ('name',)