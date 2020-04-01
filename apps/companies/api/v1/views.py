from rest_framework import generics, permissions

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


class CurrentUserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer