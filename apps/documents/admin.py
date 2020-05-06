from django.contrib import admin

# Register your models here.
from .models import (
    Document,
    DocumentTemplate,
    DocumentTemplateParam,
)


class DocumentTemplateParamInline(admin.TabularInline):
    model = DocumentTemplateParam
    fields = ('code', 'name', 'value_type', 'value', 'active')
    extra = 0


@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    model = DocumentTemplate
    fields = [
        'name',
        'file_template',
        'params',
        'company',
        'template',
        'active',
    ]
    inlines=[DocumentTemplateParamInline,]
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    model = Document
    fields = [
        'document_template',
        'id',
        'created',
    ]
    list_display = ('__str__',)
    list_display_links = ('__str__',)