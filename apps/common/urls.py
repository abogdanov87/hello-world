from django.conf.urls import url

from .api.v1 import views as api_v1_views
from . import apps

app_name = apps.AppConfig.name

urlpatterns = []
