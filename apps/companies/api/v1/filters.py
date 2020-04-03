from django_filters import rest_framework as filters
from companies.models import Company, Workplace, Department


class CompanyFilter(filters.FilterSet):
    class Meta:
        model = Company
        fields = ('active',)


class WorkplaceFilter(filters.FilterSet):
    class Meta:
        model = Workplace
        fields = ('active',)


class DepartmentFilter(filters.FilterSet):
    class Meta:
        model = Department
        fields = ('active', 'company')
