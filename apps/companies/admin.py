from django.contrib import admin

# Register your models here.
from .models import (
    Company,
    User,
    Department,
    Workplace,
    DepartmentType,
)


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


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = [
        'last_login',
        'is_superuser',
        'username',
        'is_staff',
        'is_active',
        'date_joined',
        'first_name',
        'last_name',
        'middle_name',
        'email',
        'avatar',
        'password_change_date',
        'groups',
        'user_permissions',
    ]
    list_display = ('id', 'username', 'last_name', 'first_name')
    list_display_links = ('username',)


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
        'active',
    ]
    list_display = ('name',)
    list_display_links = ('name',)