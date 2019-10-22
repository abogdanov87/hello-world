from django.conf.urls import url

from .api.v1 import views as api_v1_views

app_name = 'company'

urlpatterns = [
    url(
        r'^api/v1/company/$',
        api_v1_views.CompanyListAPIView.as_view(),
        name='company_list',
    ),
    url(
        r'^api/v1/company/(?P<pk>\d+)/$',
        api_v1_views.CompanyRetrieveUpdateAPIView.as_view(),
        name='company_detail',
    ),
]
