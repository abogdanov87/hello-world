from rest_framework import generics

from companies.models import Company, User
from .serializers import CompanySerializer, UserSerializer
from .filters import CompanyFilter


class CompanyListAPIView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter


class CompanyRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        if self.request.user.is_authenticated:
            return queryset.filter(pk=self.request.user.id)
        else:
            return queryset.filter(pk=-1)