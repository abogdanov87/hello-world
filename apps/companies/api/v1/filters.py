from django_filters import rest_framework as filters

from companies.models import Company


class CompanyFilter(filters.FilterSet):
    class Meta:
        model = Company
        fields = ('active',)
