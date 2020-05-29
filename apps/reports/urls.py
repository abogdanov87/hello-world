from django.conf.urls import url
from django.urls import path

from .api.v1 import views as api_v1_views
from . import apps

app_name = apps.ReportsConfig.name

urlpatterns = [
    url(
        r'^api/v1/reports/$',
        api_v1_views.ReportListCreateUpdateAPIView.as_view(),
        name='list',
    ),
    url(
        r'^api/v1/content-types/$',
        api_v1_views.ContentTypeListAPIView.as_view(),
        name='list',
    ),
]
