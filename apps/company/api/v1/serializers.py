from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from company.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id',
            'name',
            'short_name',
            'inn',
            'active',
        )

    def validate(self, data):
        return data
