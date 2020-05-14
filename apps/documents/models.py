import os
from django.db import models
import uuid
from django.apps import apps
from datetime import datetime, timedelta
from django.conf import settings
from common.models import Entity
from django.core.validators import FileExtensionValidator

from django.utils.translation import gettext_lazy as _


def get_file_path(instance, filename):
    return 'doc_generated/{}-{}.{}'.format(instance.document_template.name, instance.id, 'docx')


def get_path():
    return '{}{}/'.format(settings.MEDIA_ROOT, 'doc_templates')


class DocumentTemplate(Entity):
    """
        Шаблон документа 
    """
    name = models.CharField(
        _('Название'),
        max_length=255,
        blank=False, null=False,
        default='',
    )
    file_template = models.FileField(
        upload_to ='doc_templates/',
        blank=True, null=True,
        verbose_name=_('Файл шаблона'),
        validators =[FileExtensionValidator(allowed_extensions=['docx'])]
    ) 
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name=_('Компания'),
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )
    template = models.BooleanField(
        _('Шаблон'),
        blank=False, null=False,
        default=False,
    )

    class Meta:
        db_table = 'document_template'
        verbose_name = _('Шаблон документа')
        verbose_name_plural = _('Шаблоны документов')

    def __str__(self):
        return self.name

    def get_file_template_name(self):
        return self.file_template.name


class Document(models.Model):
    """ 
        Документ 
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        blank=False, null=False,
    )
    created = models.DateTimeField(
        _('Создан'), 
        default=datetime.now
    )
    document_template = models.ForeignKey(
        DocumentTemplate,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Шаблон'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Пользователь'),
    )

    class Meta:
        db_table = 'document'
        verbose_name = _('Документ')
        verbose_name_plural = _('Документы')

    def __str__(self):
        return '{} ({})'.format(self.id, self.document_template.name)