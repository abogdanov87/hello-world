import os
from django.db import models
from django.apps import apps
from datetime import datetime, timedelta
from django.conf import settings
from common.models import Entity
from django.contrib.contenttypes.models import ContentType

from django.utils.translation import gettext_lazy as _


class Report(Entity):
    """
        Отчет
    """
    name = models.CharField(
        _('Название'),
        max_length=255,
        blank=False, null=False,
        default='',
    )
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name=_('Компания'),
    )
    document_template = models.ForeignKey(
        'documents.DocumentTemplate',
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name=_('Шаблон'),
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name=_('Контент'),
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'report'
        verbose_name = _('Отчет')
        verbose_name_plural = _('Отчеты')

    def __str__(self):
        return self.name