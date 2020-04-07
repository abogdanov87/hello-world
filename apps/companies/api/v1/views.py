from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from companies.models import (
    Company, 
    User, 
    Workplace, 
    Department,
    Position,
    Equipment,
    Employee,
    DepartmentType,
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
)
from .filters import (
    CompanyFilter, 
    DepartmentFilter, 
    WorkplaceFilter,
    PositionFilter,
    EquipmentFilter,
    EmployeeFilter,
)


class CompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user.id)

    def create(self, request, *args, **kwargs):
        if request.user:
            request.data.update({
                'user': [ request.user.id ]
            })
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list),
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers,
        )


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


class DepartmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filterset_class = DepartmentFilter


class DepartmentRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentTypeListAPIView(generics.ListAPIView):
    queryset = DepartmentType.objects.all()
    serializer_class = DepartmentTypeSerializer


class PositionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    filterset_class = PositionFilter


class EquipmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filterset_class = EquipmentFilter


class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filterset_class = EmployeeFilter