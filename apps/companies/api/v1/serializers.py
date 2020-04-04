from rest_framework import serializers
from companies.models import (
    Company, 
    User, 
    Workplace, 
    Department,
    DepartmentType,
    EquipmentGroup,
    Equipment,
    Position,
    Employee
)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id',
            'name',
            'short_name',
            'inn',
            'badge',
            'user',
            'active',
        )

    def validate(self, data):
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'last_name',
            'first_name',
            'middle_name',
            'avatar',
        )

    def validate(self, data):
        return data


class DepartmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentType
        fields = (
            'id',
            'name',
            'active',
        )

    def validate(self, data):
        return data


class DepartmentSerializer(serializers.ModelSerializer):
    department_type = DepartmentTypeSerializer()

    class Meta:
        model = Department
        fields = (
            'id',
            'code',
            'name',
            'department_type',
            'parent',
            'company',
            'active',
        )

    def validate(self, data):
        return data


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = (
            'id',
            'code',
            'name',
            'company',
            'boss',
            'active',
        )

    def validate(self, data):
        return data


class EquipmentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentGroup
        fields = (
            'id',
            'name',
            'active',
        )

    def validate(self, data):
        return data


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = (
            'id',
            'code',
            'name',
            'inventory_number',
            'equipment_group',
            'company',
            'active',
        )

    def validate(self, data):
        return data


class WorkplaceSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    position = PositionSerializer()
    equipment = EquipmentSerializer(many = True)

    class Meta:
        model = Workplace
        fields = (
            'id',
            'code',
            'position',
            'department',
            'equipment',
            'instruction_required',
            'active',
        )

    def validate(self, data):
        return data


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id',
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
        )

    def validate(self, data):
        return data