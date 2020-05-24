from django_filters import rest_framework as filters
from django.db.models import Q, CharField
from django.db.models.functions import Lower
from datetime import datetime
from companies.models import (
    Company, 
    Workplace, 
    Department,
    Position,
    Equipment,
    Employee,
    Commission,
    Event,
    DepartmentType,
    EventEmployee,
    EventType,
    AssessmentCard,
)


CharField.register_lookup(Lower)


class CompanyFilter(filters.FilterSet):
    class Meta:
        model = Company
        fields = ('active',)


class WorkplaceFilter(filters.FilterSet):
    class Meta:
        model = Workplace
        fields = ('active', 'department')


class DepartmentFilter(filters.FilterSet):
    class Meta:
        model = Department
        fields = ('active', 'company')

    
class DepartmentTypeFilter(filters.FilterSet):
    class Meta:
        model = DepartmentType
        fields = ('active', 'company')


class PositionFilter(filters.FilterSet):
    class Meta:
        model = Position
        fields = ('active', 'company')


class EquipmentFilter(filters.FilterSet):
    class Meta:
        model = Equipment
        fields = ('active', 'company')


class EmployeeFilter(filters.FilterSet):
    class Meta:
        model = Employee
        fields = ('workplace', 'company')


class CommissionFilter(filters.FilterSet):
    class Meta:
        model = Commission
        fields = ('company',)


class EventFilter(filters.FilterSet):
    company = filters.NumberFilter(field_name='company', method='filter_company')
    name = filters.CharFilter(field_name='name', method='filter_name')
    employee = filters.NumberFilter(field_name='employee', method='filter_employee')
    event_date_from = filters.CharFilter(field_name='event_date_from', method='filter_event_date_from')
    event_date_to = filters.CharFilter(field_name='event_date_to', method='filter_event_date_to')

    class Meta:
        model = Event
        fields = ('company', 'name', 'active', 'event_type', 'employee', 'event_date_from', 'event_date_to')

    def filter_company(self, queryset, name, value):
        return queryset.filter(
            Q(company__isnull=True) | 
            Q(company=value)
        )

    def filter_name(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

    def filter_employee(self, queryset, name, value):
        return queryset.filter(employees__employee=value, employees__active=True)

    def filter_event_date_from(self, queryset, name, value):
        return queryset.filter(event_date__gt=datetime.strptime(value, '%Y-%m-%d'))

    def filter_event_date_to(self, queryset, name, value):
        return queryset.filter(event_date__lt=datetime.strptime(value, '%Y-%m-%d'))


class EventEmployeeFilter(filters.FilterSet):
    class Meta:
        model = EventEmployee
        fields = ('event_instance',)


class EventTypeFilter(filters.FilterSet):
    company = filters.NumberFilter(field_name='company', method='filter_company')

    class Meta:
        model = EventType
        fields = ('active', 'company')
    
    def filter_company(self, queryset, name, value):
        return queryset.filter(
            Q(company__isnull=True) | 
            Q(company=value)
        )


class AssessmentCardFilter(filters.FilterSet):
    company = filters.NumberFilter(field_name='company', method='filter_company')

    class Meta:
        model = AssessmentCard
        fields = ('active', 'company',)

    def filter_company(self, queryset, name, value):
        return queryset.filter(
            workplace__department__company=value
        )