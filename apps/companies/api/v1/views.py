from rest_framework import generics, permissions, status, filters
from rest_framework_bulk import ListBulkCreateUpdateAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from PIL import Image
import glob, os
from django.conf import settings
from django.db.models import Q, CharField
from django.http import HttpResponse, Http404, JsonResponse


from companies.models import (
    Company, 
    User, 
    Workplace, 
    Department,
    Position,
    Equipment,
    Employee,
    DepartmentType,
    CommissionEmployee,
    Commission,
    Event,
    EventEmployee,
    EventDocumentTemplate,
    EventType,
    AssessmentCard,
    WorkType,
    HarmfulFactor,
    HarmfulSubstance,
    WorkingConditionClass,
)
from .serializers import (
    CompanySerializer, 
    UserSerializer, 
    WorkplaceSerializer, 
    DepartmentSerializer,
    PositionSerializer,
    EquipmentSerializer,
    EmployeeSerializer,
    DepartmentTypeSerializer,
    CommissionEmployeeSerializer,
    CommissionSerializer,
    EventSerializer,
    EventEmployeeSerializer,
    EventDocumentTemplateSerializer,
    EventTypeSerializer,
    AssessmentCardSerializer,
    WorkTypeSerializer,
    HarmfulFactorSerializer,
    HarmfulSubstanceSerializer,
    WorkingConditionClassSerializer,
)
from .filters import (
    CompanyFilter, 
    DepartmentFilter, 
    WorkplaceFilter,
    PositionFilter,
    EquipmentFilter,
    EmployeeFilter,
    CommissionFilter,
    EventFilter,
    DepartmentTypeFilter,
    EventEmployeeFilter,
    EventTypeFilter,
    AssessmentCardFilter,
)


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'


class CompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user.id)

    def post(self, request, format=None):
        company_instance = Company(
            name=request.data['name'],
            short_name=request.data['short_name'],
            inn=request.data['inn'],
            active=True,
        )
        badge = request.FILES.get('badge', None)
        if not badge is None:
            company_instance.badge = badge
        company_instance.save()
        company_instance.user.add(request.user)
        return Response(CompanySerializer(company_instance).data, status.HTTP_201_CREATED)


class CompanyRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class MeAPIView(APIView):
    queryset = User.objects.all()

    def get(self, request, format=None):
        me = request.user
        serializer = UserSerializer(me)
        return Response(serializer.data)


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WorkplaceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Workplace.objects.all()
    serializer_class = WorkplaceSerializer
    filterset_class = WorkplaceFilter

    def get_queryset(self):
        queryset = Workplace.objects.all()
        company = self.request.query_params.get('company', None)
        if company is not None:
            queryset = queryset.filter(department__company=company)
        return queryset


class WorkplaceRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Workplace.objects.all()
    serializer_class = WorkplaceSerializer


class DepartmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filterset_class = DepartmentFilter


class DepartmentRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentTypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = DepartmentType.objects.all()
    serializer_class = DepartmentTypeSerializer
    filterset_class = DepartmentTypeFilter


class DepartmentTypeRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = DepartmentType.objects.all()
    serializer_class = DepartmentTypeSerializer


class PositionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    filterset_class = PositionFilter


class PositionRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class EquipmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filterset_class = EquipmentFilter


class EquipmentRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer


class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filterset_class = EmployeeFilter


class EmployeeRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class CommissionEmployeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = CommissionEmployee.objects.all()
    serializer_class = CommissionEmployeeSerializer
    
    def get_queryset(self):
        queryset = CommissionEmployee.objects.all()
        company = self.request.query_params.get('company', None)
        if company is not None:
            queryset = queryset.filter(commission__company=company)
        return queryset


class CommissionEmployeeRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = CommissionEmployee.objects.all()
    serializer_class = CommissionEmployeeSerializer
    
    def get_queryset(self):
        queryset = CommissionEmployee.objects.all()
        company = self.request.query_params.get('company', None)
        if company is not None:
            queryset = queryset.filter(commission__company=company)
        return queryset


class CommissionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    filterset_class = CommissionFilter


class CommissionRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer


class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('-event_date')
    serializer_class = EventSerializer
    filterset_class = EventFilter
    pagination_class = CustomPageNumberPagination


class EventRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventEmployeeListCreateAPIView(ListBulkCreateUpdateAPIView):
    queryset = EventEmployee.objects.all()
    serializer_class = EventEmployeeSerializer
    filterset_class = EventEmployeeFilter
    
    def get_queryset(self):
        queryset = EventEmployee.objects.all()
        company = self.request.query_params.get('company', None)
        if company is not None:
            queryset = queryset.filter(event_instance__company=company)
        return queryset


class EventDocumentTemplateListCreateAPIView(ListBulkCreateUpdateAPIView):
    queryset = EventDocumentTemplate.objects.all()
    serializer_class = EventDocumentTemplateSerializer
    
    def get_queryset(self):
        queryset = EventDocumentTemplate.objects.all()
        company = self.request.query_params.get('company', None)
        if company is not None:
            queryset = queryset.filter(event__company=company)
        return queryset


class EventDocumentTemplateRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = EventDocumentTemplate.objects.all()
    serializer_class = EventDocumentTemplateSerializer

    def get_queryset(self):
        queryset = EventDocumentTemplate.objects.all()
        company = self.request.query_params.get('company', None)
        if company is not None:
            queryset = queryset.filter(event__company=company)
        return queryset


class EventTypeListCreateAPIView(ListBulkCreateUpdateAPIView):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    filterset_class = EventTypeFilter


class AssessmentCardListCreateUpdateAPIView(ListBulkCreateUpdateAPIView):
    queryset = AssessmentCard.objects.all()
    serializer_class = AssessmentCardSerializer
    filterset_class = AssessmentCardFilter


class DictListAPIView(generics.ListAPIView):
    queryset = WorkType.objects.all()

    def get(self, request, format=None):
        working_condition_class_queryset = WorkingConditionClass.objects.all()
        work_type_queryset = WorkType.objects.all()
        harmful_factor_queryset = HarmfulFactor.objects.all()
        harmful_substance_queryset = HarmfulSubstance.objects.all()
        working_condition_class_serializer = WorkingConditionClassSerializer(working_condition_class_queryset, many=True)
        work_type_serializer = WorkTypeSerializer(work_type_queryset, many=True)
        harmful_factor_serializer = WorkTypeSerializer(harmful_factor_queryset, many=True)
        harmful_substance_serializer = WorkTypeSerializer(harmful_substance_queryset, many=True)
        return Response({
            'working_condition_classes': working_condition_class_serializer.data,
            'work_types': work_type_serializer.data,
            'harmful_factors': harmful_factor_serializer.data,
            'harmful_substances': harmful_substance_serializer.data,
        }, status.HTTP_200_OK)