from django.conf.urls import url

from .api.v1 import views as api_v1_views
from . import apps

app_name = apps.CommonConfig.name

urlpatterns = [
    url(
        r'^api/v1/params/$',
        api_v1_views.ParamListCreateAPIView.as_view(),
        name='list',
    ),
    url(
        r'^api/v1/params/(?P<pk>\d+)/$',
        api_v1_views.ParamRetrieveUpdateAPIView.as_view(),
        name='detail',
    ),
]