from django_filters import rest_framework as filters
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
)


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
    class Meta:
        model = Event
        fields = ('company',)


class EventEmployeeFilter(filters.FilterSet):
    class Meta:
        model = EventEmployee
        fields = ('event_instance',)