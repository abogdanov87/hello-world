from rest_framework import serializers
# from drf_writable_nested import WritableNestedModelSerializer
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


class EventDocumentTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDocumentTemplate
        fields = (
            'id',
            # 'event',
            'document_template',
            'apply_to',
            'active',
        )


class EventSerializer(serializers.ModelSerializer):
    # params = ParamSerializer(many=True)
    document_template = EventDocumentTemplateSerializer(
        source='event_to_doc_template',
        many=True
    )

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
            # 'params',
            'document_template',
            'previous',
            'active',
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['employee'] = EmployeeSerializer(
            instance.employee, many=True
        ).data
        q = EventDocumentTemplate.objects.filter(event=instance.pk)
        response['document_template'] = EventDocumentTemplateSerializer(
            q, many=True
        ).data
        return response

    def create(self, validated_data):
        document_template_data = validated_data.pop('event_to_doc_template')
        instance = Event(
            event_type=validated_data.get('event_type', None),
            name=validated_data.get('name', None),
            event_date=validated_data.get('event_date', None),
            frequency=validated_data.get('frequency', None),
            company=validated_data.get('company', None),
            commission=validated_data.get('commission', None),
            previous=validated_data.get('previous', None),
            active=validated_data.get('active', None),
        )
        instance.save()
        for dtd in document_template_data:
            dt_instance = EventDocumentTemplate()
            dt_instance.event = instance
            dt_instance.document_template = dtd.get('document_template', None)
            dt_instance.apply_to = dtd.get('apply_to', None)
            dt_instance.active = dtd.get('active', None)
            dt_instance.save()

        return instance

    def update(self, instance, validated_data):
        document_template_data = validated_data.pop('event_to_doc_template')
        document_template = instance.event_to_doc_template

        instance.event_type = validated_data.get('event_type', instance.event_type)
        instance.name = validated_data.get('name', instance.name)
        instance.event_date = validated_data.get('event_date', instance.event_date)
        instance.frequency = validated_data.get('frequency', instance.frequency)
        instance.company = validated_data.get('company', instance.company)
        instance.commission = validated_data.get('commission', instance.commission)
        instance.previous = validated_data.get('previous', instance.previous)
        instance.active = validated_data.get('active', instance.active)
        instance.save()

        for dtd in document_template_data:
            if EventDocumentTemplate.objects.filter(
                event=instance.id,
                document_template=dtd.get('document_template', None).id,
            ).exists():
                dt_instance = EventDocumentTemplate.objects.filter(
                    event=instance.id,
                    document_template=dtd.get('document_template', None).id,
                ).first()
            else:
                dt_instance = EventDocumentTemplate()
            dt_instance.event = instance
            dt_instance.document_template = dtd.get('document_template', None)
            dt_instance.apply_to = dtd.get('apply_to', None)
            dt_instance.active = dtd.get('active', None)
            dt_instance.save()

        return instance

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