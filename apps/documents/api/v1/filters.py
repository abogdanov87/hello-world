from django_filters import rest_framework as filters
from documents.models import (
    DocumentTemplate,
)


class DocumentTemplateFilter(filters.FilterSet):
    class Meta:
        model = DocumentTemplate
        fields = ('company',)