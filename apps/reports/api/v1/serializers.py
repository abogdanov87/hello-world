from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin
from django.contrib.contenttypes.models import ContentType
from reports.models import (
    Report,
)


class ReportSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Report
        list_serializer_class = BulkListSerializer
        fields = (
            'id',
            'name',
            'company',
            'document_template',
            'content_type',
            'active',
        )

    def validate(self, data):
        return data


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = (
            'id',
            'name',
        )