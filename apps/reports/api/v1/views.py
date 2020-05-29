import os
from rest_framework import generics, permissions, status
from rest_framework_bulk import ListBulkCreateUpdateAPIView
from django.conf import settings
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


from .serializers import (
    ReportSerializer,
    ContentTypeSerializer,
)
from .filters import (
    ReportFilter,
)
from reports.models import (
    Report,
)


class ReportListCreateUpdateAPIView(ListBulkCreateUpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filterset_class = ReportFilter


class ContentTypeListAPIView(generics.ListAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer

    def get_queryset(self):
        queryset = ContentType.objects.filter(
            model__in=[
                'company', 
                'event',
                'documenttemplate',
                'employee',
                'workplace',
            ]
        )
        return queryset