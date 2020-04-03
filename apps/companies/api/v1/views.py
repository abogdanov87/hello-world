from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from companies.models import Company, User, Workplace, Department
from .serializers import CompanySerializer, UserSerializer, WorkplaceSerializer, DepartmentSerializer
from .filters import CompanyFilter, DepartmentFilter, WorkplaceFilter


class CompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user.id)


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
        return Workplace.objects.all()


class DepartmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filterset_class = DepartmentFilter