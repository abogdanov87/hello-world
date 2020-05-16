from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
from .models import (
    Company,
    User,
    Department,
    Workplace,
    DepartmentType,
    EquipmentGroup,
    Equipment,
    Position,
    Employee,
    CommissionEmployee,
    Commission,
    EventType,
    Event,
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    fields = [
        'event_type',
        'name',
        'event_date',
        'frequency',
        'company',
        'commission',
        'previous',
        'active',
    ]
    list_display = ('name', 'company',)
    list_display_links = ('name',)


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    model = EventType
    fields = [
        'name',
        'company',
        'active',
    ]
    list_display = ('name', 'company',)
    list_display_links = ('name',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company
    fields = [
        'name',
        'short_name',
        'inn',
        'badge',
        'active',
        'user',
    ]
    list_display = ('name', 'inn',)
    list_display_links = ('name',)


class MyUserAdmin(UserAdmin):
    model = User
    list_display = (
        'id', 
        'username', 
        'last_name', 
        'first_name',
        'middle_name',
        'avatar',
    )
    list_display_links = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            _('Личные данные'),
            {
                'fields': (
                    'last_name',
                    'first_name',
                    'middle_name',
                    'avatar',
                ),
            },
        ),
        (
            _('Доступы'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
    )


admin.site.register(User, MyUserAdmin)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    model = Department
    fields = [
        'code',
        'name',
        'department_type',
        'parent',
        'company',
        'active',
    ]
    list_display = ('code', 'name', 'company')
    list_display_links = ('code', 'name')


@admin.register(DepartmentType)
class DepartmentTypeAdmin(admin.ModelAdmin):
    model = DepartmentType
    fields = [
        'name',
        'order_num',
        'active',
    ]
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(EquipmentGroup)
class EquipmentGroupAdmin(admin.ModelAdmin):
    model = EquipmentGroup
    fields = [
        'name',
        'active',
    ]
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    model = Equipment
    fields = [
        'code',
        'name',
        'inventory_number',
        'equipment_group',
        'company',
        'active',
    ]
    list_display = ('code', 'name', 'company')
    list_display_links = ('code', 'name')


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    model = Equipment
    fields = [
        'code',
        'name',
        'company',
        'boss',
        'company_boss',
        'active',
    ]
    list_display = ('code', 'name', 'company')
    list_display_links = ('code',)


@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    model = Workplace
    fields = [
        'code',
        'position',
        'department',
        'equipment',
        'instruction_required',
        'active',
    ]
    list_display = ('code', 'position_name', 'department_name', 'company_name')
    list_display_links = ('code', 'position_name', 'department_name', 'company_name')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    fields = [
        'last_name',
        'first_name',
        'middle_name',
        'address',
        'birth_date',
        'gender',
        'disability',
        'employment_date',
        'pers_number',
        'avatar',
        'insurance_number',
        'workplace',
        'fire_date',
        'company',
    ]
    list_display = ('pers_number', '__str__', 'company_name')
    list_display_links = ('pers_number', '__str__',)


@admin.register(CommissionEmployee)
class CommissionEmployeeAdmin(admin.ModelAdmin):
    model = CommissionEmployee
    fields = [
        'commission',
        'employee',
        'member_status',
        'active',
    ]
    list_display = ('__str__',)
    list_display_links = ('__str__',)


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    fields = [
        'num',
        'name',
        'decree',
        'decree_date',
        'document_template',
        'active',
    ]
    list_display = ('__str__',)
    list_display_links = ('__str__',)