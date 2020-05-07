from rest_framework import serializers
from common.models import (
    Param,
)


class ParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Param
        fields = (
            'id',
            'code',
            'name',
            'value_type',
            'value',
            'entity',
            'active',
        )

    def validate(self, data):
        return data