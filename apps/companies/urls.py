from django.conf.urls import url

from .api.v1 import views as api_v1_views
from . import apps

app_name = apps.CompanyConfig.name

urlpatterns = [
    url(
        r'^api/v1/me/$',
        api_v1_views.MeAPIView.as_view(),
        name='me',
    ),
    url(
        r'^api/v1/companies/$',
        api_v1_views.CompanyListCreateAPIView.as_view(),
        name='list',
    ),
    url(
        r'^api/v1/companies/(?P<pk>\d+)/$',
        api_v1_views.CompanyRetrieveUpdateAPIView.as_view(),
        name='detail',
    ),
    url(
        r'^api/v1/users/(?P<pk>\d+)/$',
        api_v1_views.UserRetrieveUpdateAPIView.as_view(),
        name='detail',
    ),
    url(
        r'^api/v1/workplaces/$',
        api_v1_views.WorkplaceListCreateAPIView.as_view(),
        name='list',
    ),
    url(
        r'^api/v1/workplaces/(?P<pk>\d+)/$',
        api_v1_views.WorkplaceRetrieveUpdateAPIView.as_view(),
        name='detail',
    ),
    url(
        r'^api/v1/departments/$',
        api_v1_views.DepartmentListCreateAPIView.as_view(),
        name='list',
    ),
    url(
        r'^api/v1/departments/(?P<pk>\d+)/$',
        api_v1_views.DepartmentRetrieveUpdateAPIView.as_view(),
        name='detail',
    ),
    url(
        r'^api/v1/positions/$',
        api_v1_views.PositionListCreateAPIView.as_view(),
        name='list',
    ),
    url(
        r'^api/v1/positions/(?P<pk>\d+)/$',
        api_v1_views.PositionRetrieveUpdateAPIView.as_view(),
        name='detail',
    ),
    url(
        r'^api/v1/equipments/$',
        api_v1_views.EquipmentListCreateAPIView.as_view(),
        name='list',
    ),
    url(
        r'^api/v1/equipments/(?P<pk>\d+)/$',
        api_v1_views.EquipmentRetrieveUpdateAPIView.as_view(),
        name='detail',
    ),
    url(
        r'^api/v1/employees/$',
        api_v1_views.EmployeeListCreateAPIView.as_view(),
        name='list',
    ),
    url(
        r'^api/v1/employees/(?P<pk>\d+)/$',
        api_v1_views.EmployeeRetrieveUpdateAPIView.as_view(),
        name='detail',
    ),
    url(
        r'^api/v1/department-types/$',
        api_v1_views.DepartmentTypeListAPIView.as_view(),
        name='list',
    ),
]
