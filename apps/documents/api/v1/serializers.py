from rest_framework import serializers
from documents.models import (
    DocumentTemplate,
    Document,
)


class DocumentTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTemplate
        fields = (
            'id',
            'name',
            'file_template',
            'get_file_template_name',
            'params',
            'company',
            'active',
        )

    def validate(self, data):
        return data


class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose')

    class Meta:
        model = Document
        fields = (
            'id',
            'created',
            'document_template',
            'user',
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['document_template'] = DocumentTemplateSerializer(
            instance.document_template,
        ).data
        return response

    def validate(self, data):
        return data