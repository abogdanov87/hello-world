from rest_framework import serializers
from companies.models import (
    Company, 
    User, 
    Workplace, 
    Department,
    DepartmentType
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


class WorkplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workplace
        fields = (
            'id',
            'code',
            'name',
            'position',
            'department',
            'equipment',
            'instruction_required',
            'active',
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