from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin
from apps.documents.api.v1.serializers import (
    DocumentTemplateSerializer,
)
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
    EventDocumentTemplate,
    EventType,
    HarmfulFactor,
    WorkType,
    HarmfulSubstance,
    AssessmentCard,
)
from documents.models import (
    DocumentTemplate,   
)
from common.api.v1.serializers import (
    ParamSerializer,
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
            'company',
            'active',
        )

    def validate(self, data):
        return data


class EventTypeSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = EventType
        list_serializer_class = BulkListSerializer
        fields = (
            'id',
            'name',
            'company',
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
            'company_boss',
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

    def validate(self, data):
        return data


class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        fields = (
            'id',
            'num',
            'name',
            'decree',
            'decree_date',
            'company',
            'active',
        )

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


class EventDocumentTemplateSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = EventDocumentTemplate
        list_serializer_class = BulkListSerializer
        fields = (
            'id',
            'event',
            'document_template',
            'apply_to',
            'active',
        )


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
            'previous',
            'active',
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

    def validate(self, data):
        return data


class EventEmployeeSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = EventEmployee
        list_serializer_class = BulkListSerializer
        fields = (
            'id',
            'event_instance',
            'employee',
            'event_date',
            'certificate',
            'active',
        )
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['event_instance'] = EventSerializer(
            instance.event_instance,
        ).data
        response['employee'] = EmployeeSerializer(
            instance.employee,
        ).data
        return response

    def validate(self, data):
        return data


class HarmfulFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarmfulFactor
        fields = (
            'code', 
            'name', 
            'inspection_frequency',
        )


class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = (
            'code', 
            'name', 
            'inspection_frequency',
        )


class HarmfulSubstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarmfulSubstance
        fields = (
            'name', 
        )


class AssessmentCardSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    harmful_factor = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=HarmfulFactor.objects.all(),
        required=False,
        allow_empty=True,
    )
    work_type = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=WorkType.objects.all(),
        required=False,
        allow_empty=True,
    )
    harmful_substance = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=HarmfulSubstance.objects.all(),
        required=False,
        allow_empty=True,
    )

    class Meta:
        model = AssessmentCard
        list_serializer_class = BulkListSerializer
        fields = (
            'card_number', 
            'workplace', 
            'working_condition_class', 
            'signing_date',
            'next_assessment_date',
            'harmful_factor',
            'work_type',
            'harmful_substance',
            'increased_pay',
            'extra_vacation',
            'reduced_working_hours',
            'milk',
            'therapeutic_nutrition',
            'early_retirement',
            'active',
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['harmful_factor'] = HarmfulFactorSerializer(
            instance.harmful_factor,
        ).data
        response['work_type'] = WorkTypeSerializer(
            instance.work_type,
        ).data
        response['harmful_substance'] = HarmfulSubstanceSerializer(
            instance.harmful_substance,
        ).data
        return response

    def validate(self, data):
        return data