from django_filters import rest_framework as filters
from django.db.models import Q
from reports.models import (
    Report,
)


class ReportFilter(filters.FilterSet):
    company = filters.NumberFilter(field_name='company', method='filter_company')

    class Meta:
        model = Report
        fields = ('company',)

    def filter_company(self, queryset, name, value):
        return queryset.filter(
            Q(company__isnull=True) | 
            Q(company=value)
        )