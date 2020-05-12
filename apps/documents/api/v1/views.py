import os
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponse, Http404, JsonResponse
from django.db.models import Max
from docxtpl import DocxTemplate
from django.conf import settings
from django.core import serializers
import uuid
import random
import json
from transliterate import translit, get_available_language_codes

from companies.models import (
    Company,
    Commission,
    Event,
)
from companies.api.v1.serializers import (
    CompanySerializer,
    CommissionSerializer,
)
from documents.models import (
    DocumentTemplate,
    Document,
)
from .serializers import (
    DocumentTemplateSerializer,
    DocumentSerializer,
)
from .filters import (
    DocumentTemplateFilter,
)
from common.models import (
    Param,
)
from common.api.v1.serializers import (
    ParamSerializer,
)


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'


def getContext(request, company_id):
    data = {}
    variables = []
    try:
        # Company
        json_data = json.loads(serializers.serialize('json', Company.objects.filter(pk=company_id)))[0]
        model_name = json_data['model'].split('.')[1]
        model_fields = json_data['fields']
        for key in model_fields:
            new_key = model_name + '_' + key
            data[new_key] = model_fields[key]
            variables.append(new_key)
        # DocumentTemplate
        json_data = json.loads(serializers.serialize('json', DocumentTemplate.objects.filter(pk=request.data['document_template'])))[0]
        model_name = json_data['model'].split('.')[1]
        model_fields = json_data['fields']
        for key in model_fields:
            new_key = model_name + '_' + key
            data[new_key] = model_fields[key]
            variables.append(new_key)
        # Event
        if request.data['entity_name'] == 'event':
            json_data = json.loads(serializers.serialize('json', Event.objects.filter(pk=request.data['entity_id'])))[0]
            model_name = json_data['model'].split('.')[1]
            model_fields = json_data['fields']
            for key in model_fields:
                new_key = model_name + '_' + key
                data[new_key] = model_fields[key]
                variables.append(new_key)

        data['variables'] = variables
        return data
    except Exception as e:
        return {'error': 'error'}


class TemplateVariableAPIView(APIView):
    queryset = DocumentTemplate.objects.all()

    def get(self, request, format=None):
        company = Company.objects.filter(pk=request.data['company'])
        company_data = CompanySerializer(company).data
        return Response({
            'company_name': company_data['name'],
            'company_inn': company_data['inn'],
        }, status.HTTP_200_OK)


class DocumentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    )

    def get(self, request, pk, format=None):
        super_get = super().get(request, pk, format)
        file_path = os.path.join(
            settings.MEDIA_ROOT, 
            'doc_generated', 
            '{}-{}.{}'.format(
                super_get.data['document_template']['name'], 
                super_get.data['id'], 
                'docx'
            ),
        )
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        return Response({ 'error': 'The file does not exist!', 'data': super_get.data }, status.HTTP_404_NOT_FOUND)


class DocumentCreateAPIView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get(self, request, format=None):
        queryset = Document.objects.filter(user=request.user.id).order_by('-created')[:11]
        serializer = DocumentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        new_id = uuid.uuid4()
        request.data.update({
            'id': new_id,
            'user': request.user.id,
        })
        resp = super().post(request, format)
        doc = DocxTemplate(os.path.join(settings.MEDIA_ROOT, resp.data['document_template']['get_file_template_name']))
        context = getContext(request, resp.data['document_template']['company'])
        doc.render(context)
        file_name = '{}-{}.docx'.format(resp.data['document_template']['name'], new_id)
        doc.save(os.path.join(settings.MEDIA_ROOT, 'doc_generated', file_name))
        resp.data.update({'context': context})
        return Response(resp.data, status.HTTP_201_CREATED)


class DocumentTemplateListCreateAPIView(generics.ListCreateAPIView):
    queryset = DocumentTemplate.objects.all()
    serializer_class = DocumentTemplateSerializer
    filterset_class = DocumentTemplateFilter
    pagination_class = CustomPageNumberPagination


class DocumentTemplateRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = DocumentTemplate.objects.all()
    serializer_class = DocumentTemplateSerializer

    def get(self, request, pk, format=None):
        super_get = super().get(request, pk, format)
        file_path = os.path.join(
            settings.MEDIA_ROOT, 
            '{}'.format(
                super_get.data['get_file_template_name'], 
            ),
        )
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        return Response({ 
                'error': 'The file does not exist!', 
                'data': super_get.data,
            }, 
            status.HTTP_404_NOT_FOUND
        )