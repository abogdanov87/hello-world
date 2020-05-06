import os
from django.db import models
import uuid
from datetime import datetime, timedelta
from companies.models import Company
from django.conf import settings

from django.utils.translation import gettext_lazy as _


def get_file_path(instance, filename):
    return 'doc_generated/{}-{}.{}'.format(instance.document_template.name, instance.id, 'docx')


def get_path():
    return '{}{}/'.format(settings.MEDIA_ROOT, 'doc_templates')


class DocumentTemplate(models.Model):
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
    ) 
    params = models.CharField(
        _('Параметры'),
        max_length=2000,
        blank=True, null=True,
    )
    company = models.ForeignKey(
        Company,
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


class DocumentTemplateParam(models.Model):
    """
        Дополнительный параметр шаблона документа 
    """
    VALUE_TYPES = (
        ('number', 'Число'),
        ('text', 'Строка'),
        ('date', 'Дата'),
        ('boolean', 'Булево'),
    )

    code = models.CharField(
        _('Код'),
        max_length=255,
        blank=False, null=False,
        default='',
    )
    name = models.CharField(
        _('Название'),
        max_length=255,
        blank=False, null=False,
        default='',
    )
    value_type = models.CharField(
        _('Формат значения'),
        max_length=10,
        choices=VALUE_TYPES,
        blank=False, null=False,
        default='number',
    )
    value = models.CharField(
        _('Значение'),
        max_length=2000,
        blank=True, null=True,
    )
    document_template = models.ForeignKey(
        DocumentTemplate,
        on_delete=models.PROTECT,
        related_name='document_template_params',
        blank=False, null=False,
        verbose_name=_('Шаблон'),
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'document_template_param'
        verbose_name = _('Параметр шаблона документа')
        verbose_name_plural = _('Параметры шаблона документа')

    def __str__(self):
        return '{} ({})'.format(self.name, self.document_template.name)


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