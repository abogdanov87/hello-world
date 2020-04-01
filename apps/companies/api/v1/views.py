from rest_framework import generics, permissions

from companies.models import Company, User
from .serializers import CompanySerializer, UserSerializer
from .filters import CompanyFilter


class CompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user.id)


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