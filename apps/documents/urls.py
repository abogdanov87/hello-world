from django.conf.urls import url
from django.urls import path

from .api.v1 import views as api_v1_views
from . import apps

app_name = apps.DocumentsConfig.name

urlpatterns = [
    url(
        r'^api/v1/document-templates/$',
        api_v1_views.DocumentTemplateListCreateAPIView.as_view(),
        name='list',
    ),
    url(
        r'^api/v1/document-templates/(?P<pk>\d+)/$',
        api_v1_views.DocumentTemplateRetrieveUpdateAPIView.as_view(),
        name='detail',
    ),
    path(
        route='documents/<uuid:pk>/',
        view=api_v1_views.DocumentRetrieveAPIView.as_view(),
        name='download',
    ),
    url(
        r'^api/v1/documents/$',
        api_v1_views.DocumentCreateAPIView.as_view(),
        name='create',
    ),
    url(
        r'^api/v1/template-variables/$',
        api_v1_views.TemplateVariableAPIView.as_view(),
        name='create',
    ),
]
