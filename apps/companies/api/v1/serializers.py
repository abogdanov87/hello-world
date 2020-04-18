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
    Employee,
    CommissionEmployee,
    Commission,
    Event,
    EventEmployee,
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
            'order_num',
            'active',
        )

    def validate(self, data):
        return data


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            'id',
            'code',
            'name',
            'department_type',
            'parent',
            'company',
            'order_num',
            'active',
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['department_type'] = DepartmentTypeSerializer(
            instance.department_type,
        ).data
        return response

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
    equipment = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Equipment.objects.all(),
        required=False,
        allow_empty=True,
    )
    employees = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Employee.objects.all(),
        required=False,
        allow_empty=True,
    ) 

    class Meta:
        model = Workplace
        fields = ( 
            'id',
            'code',
            'position',
            'department',
            'instruction_required',
            'equipment',
            'employees',
            'active',
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['department'] = DepartmentSerializer(
            instance.department,
        ).data
        response['position'] = PositionSerializer(
            instance.position,
        ).data
        response['equipment_list'] = EquipmentSerializer(
            instance.equipment, many=True
        ).data
        return response

    def update(self, instance, validated_data):
        if validated_data.get('equipment'):
            equipments = validated_data.pop('equipment')
            instance.equipment.clear()
            for equipment in equipments:
                instance.equipment.add(equipment)

        instance = super().update(instance, validated_data)
        return instance

    def validate(self, data):
        return data


class EmployeeSerializer(serializers.ModelSerializer):
    workplace = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Workplace.objects.all(),
        required=False,
        allow_empty=True,
    )

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
            'workplace',
            'insurance_number',
            'fire_date',
            'company',
        )

    def update(self, instance, validated_data):
        if validated_data.get('workplace'):
            workplaces = validated_data.pop('workplace')
            instance.workplace.clear()
            for workplace in workplaces:
                instance.workplace.add(workplace)

        instance = super().update(instance, validated_data)
        return instance

    def validate(self, data):
        return data


class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        fields = (
            'id',
            'num',
            'commission_type',
            'name',
            'decree',
            'decree_date',
            'company',
            'active',
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

    def validate(self, data):
        return data


class CommissionEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionEmployee
        fields = (
            'id',
            'commission',
            'employee',
            'member_status',
            'active',
        )
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['commission'] = CommissionSerializer(
            instance.commission,
        ).data
        response['employee'] = EmployeeSerializer(
            instance.employee,
        ).data
        return response

    def validate(self, data):
        return data


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id',
            'event_type',
            'name',
            'event_date',
            'frequency',
            'company',
            'commission',
            'active',
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['employee'] = EmployeeSerializer(
            instance.employee, many=True
        ).data
        return response

    def validate(self, data):
        return data


class EventEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventEmployee
        fields = (
            'id',
            'event',
            'employee',
            'event_date',
            'certificate',
            'active',
        )
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['event'] = EventSerializer(
            instance.event,
        ).data
        response['employee'] = EmployeeSerializer(
            instance.employee,
        ).data
        return response

    def validate(self, data):
        return data