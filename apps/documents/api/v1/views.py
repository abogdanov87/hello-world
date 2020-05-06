import os
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, Http404, JsonResponse
from django.db.models import Max
from docxtpl import DocxTemplate
from django.conf import settings
import uuid
import random
import json
from transliterate import translit, get_available_language_codes

from companies.models import (
    Company,
    Commission,
)
from companies.api.v1.serializers import (
    CompanySerializer,
    CommissionSerializer,
)
from documents.models import (
    DocumentTemplate,
    Document,
    DocumentTemplateParam,
)
from .serializers import (
    DocumentTemplateSerializer,
    DocumentTemplateParamSerializer,
    DocumentSerializer,
)
from .filters import (
    DocumentTemplateFilter,
)


def getContext(request, company_id):
    company = Company.objects.get(pk=company_id)
    try:
        response_data = {
            'company_name': company.name,
            'company_inn': company.inn,
        }
        return response_data
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
        queryset = Document.objects.filter(user=request.user.id)
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
        return Response(resp.data, status.HTTP_201_CREATED)


class DocumentTemplateListCreateAPIView(generics.ListCreateAPIView):
    queryset = DocumentTemplate.objects.all()
    serializer_class = DocumentTemplateSerializer
    filterset_class = DocumentTemplateFilter

    def post(self, request, format=None):
        try:
            active = str(request.data.get('active', True)).lower() == 'true'
            template = request.FILES.get('file', None)
            is_new = True if request.data.get('id', None) is None else False
            if is_new:
                if template is None:
                    instance = DocumentTemplate(
                        id=request.data.get('id', None),
                        name=request.data.get('file_name', request.data['name']),
                        company=Company.objects.get(pk=request.data['company']),
                        params=request.data.get('params', None),
                        active=active,
                        template=False,
                    )
                else :
                    instance = DocumentTemplate(
                        id=request.data.get('id', None),
                        name=request.data.get('file_name', request.data['name']),
                        file_template=template,
                        company=Company.objects.get(pk=request.data['company']),
                        params=request.data.get('params', None),
                        active=active,
                        template=False,
                    )
            else:
                instance = DocumentTemplate.objects.get(pk=request.data.get('id', None))
                instance.name = request.data.get('file_name', request.data['name'])
                instance.params = request.data.get('params', None)
                instance.active = active
                if not template is None: 
                    instance.file_template = template
            instance.save()
            document_template_params = json.loads(request.data.get('document_template_params', None))
            if not document_template_params is None and instance:
                for dtp in document_template_params:
                    dtp.update({
                        'code': translit(dtp['name'], 'ru', reversed=True).lower().replace(' ', '_').replace('%', 'percent'),
                        'value': '' if str(dtp['value']) == 'None' else str(dtp['value']),
                        'document_template': instance.id
                    })
                    if not dtp.get('id', None) is None and dtp.get('id', None) > 0:
                        dtp_instance = DocumentTemplateParam.objects.get(pk=dtp['id'])
                        dtp_serializer = DocumentTemplateParamSerializer(dtp_instance, data=dtp)
                    else:
                        dtp_serializer = DocumentTemplateParamSerializer(data=dtp)
                    if dtp_serializer.is_valid():
                        dtp_serializer.save()
            if not request.data.get('commission', None) is None and instance:
                commission = Commission.objects.get(pk=request.data['commission'])
                commission.document_template = instance
                commission.save()
            return Response(DocumentTemplateSerializer(instance).data, status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)


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