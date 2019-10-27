from rest_framework import serializers

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
