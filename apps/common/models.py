from django.db import models

from django.utils.translation import gettext_lazy as _


class Entity(models.Model):
    """
        Абстрактная сущность
    """
    pass


class Param(models.Model):
    """
        Дополнительный параметр
    """
    VALUE_TYPES = (
        ('text', 'Строка'),
        ('number', 'Число'),
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
        default='text',
    )
    value = models.CharField(
        _('Значение'),
        max_length=2000,
        blank=True, null=True,
    )
    entity = models.ForeignKey(
        Entity,
        on_delete=models.PROTECT,
        related_name='params',
        blank=False, null=False,
        verbose_name=_('Сущность'),
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'param'
        verbose_name = _('Дополнительный параметр')
        verbose_name_plural = _('Дополнительные параметры')

    def __str__(self):
        return '{} ({})'.format(self.name, self.entity.__str__)