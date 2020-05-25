import os
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone
from django.conf import settings
from easy_thumbnails.fields import ThumbnailerImageField
from django.apps import apps
from common.models import Entity, PeriodHistoricalModel
from simple_history.models import HistoricalRecords

from django.utils.translation import gettext_lazy as _


INSPECTION_FREQUENCY = (
    ('10 1t/1y', '1 раз в год'),
    ('20 1t/2y', '1 раз в 2 года'),
)


CATEGORY = (
    ('chemical', 'Химический'), 
    ('biological', 'Биологический'),
    ('industrial aerosols', 'Промышленный аэрозоли'),
    ('physical', 'Физические'),
    ('ongoing work', 'Проводимые работы. Категории должностей.'),
)


class User(AbstractUser):
    """
        CustomUser
    """

    first_name = models.CharField(
        _('Имя'),
        max_length=30,
        blank=True, null=True,
    )
    last_name = models.CharField(
        _('Фамилия'),
        max_length=30,
        blank=True, null=True,
    )
    middle_name = models.CharField(
        _('Отчество'),
        max_length=30,
        blank=True, null=True,
    )
    email = models.EmailField(
        _('Адрес электронной почты'),
        blank=True, null=True,
    )
    avatar = ThumbnailerImageField(
        _('Аватарка'),
        upload_to ='avatars/',
        blank=True, null=True,
        resize_source=dict(size=(128, 128), sharpen=True),
    )
    password_change_date = models.DateTimeField(
        _('Дата изменения пароля'),
        default=timezone.datetime(year=1970, month=1, day=1),
    )

    class Meta:
        db_table = 'auth_user'
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')


class Company(models.Model):
    """
        Компания 
    """
    name = models.CharField(
        _('Название'),
        max_length=255,
        blank=False, null=False,
        default='',
    )
    short_name = models.CharField(
        _('Краткое название'),
        max_length=255,
        blank=False, null=False,
        default='',
    )
    inn = models.CharField(
        _('ИНН'),
        max_length=20,
        blank=False, null=False,
        default='',
    )
    badge = ThumbnailerImageField(
        _('Логотип'),
        upload_to ='badges/',
        blank=True, null=True,
        resize_source=dict(size=(128, 128), sharpen=True),
    )
    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Пользователь'),
        related_name='user_companies',
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )
    history = HistoricalRecords()

    class Meta:
        db_table = 'company'
        verbose_name = _('Компания')
        verbose_name_plural = _('Компании')

    def __str__(self):
        return self.name


class DepartmentType(models.Model):
    """
        Тип подразделения
    """
    name = models.CharField(
        _('Название'),
        max_length=255,
        blank=False, null=False,
        default='',
    )
    order_num = models.PositiveIntegerField(
        _('Порядок'),
        blank=False, null=False,
        default=1,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Компания'),
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'department_type'
        verbose_name = _('Тип подразделения')
        verbose_name_plural = _('Типы подразделений')

    def __str__(self):
        return self.name


class Department(models.Model):
    """
        Подразделение
    """
    code = models.CharField(
        _('Код подразделения'),
        max_length=30,
        blank=True, null=True,
    )
    name = models.CharField(
        _('Название'),
        max_length=2000,
        blank=False, null=False,
        default='',
    )
    department_type = models.ForeignKey(
        DepartmentType,
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name=_('Тип подразделения'),
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name=_('Вышестоящее подразделение'),
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Компания'),
    )
    order_num = models.PositiveIntegerField(
        _('Порядок'),
        blank=False, null=False,
        default=1,
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'department'
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'

    def __str__(self):
        return self.name


class Position(models.Model):
    """
        Должность
    """
    code = models.CharField(
        _('Код должности'),
        max_length=30,
        blank=True, null=True,
    )
    name = models.CharField(
        _('Название'),
        max_length=2000,
        blank=False, null=False,
        default='',
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Компания'),
    )
    boss = models.BooleanField(
        _('Руководящая позиция'),
        blank=False, null=False,
        default=False,
    )
    company_boss = models.BooleanField(
        _('Руководитель компании'),
        blank=False, null=False,
        default=False,
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'position'
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.name


class EquipmentGroup(models.Model):
    """
        Группа инструмента
    """
    name = models.CharField(
        _('Название'),
        max_length=2000,
        blank=False, null=False,
        default='',
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'equipment_group'
        verbose_name = 'Группа инструментов'
        verbose_name_plural = 'Группы инструментов'


class Equipment(models.Model):
    """
        Инструмент
    """
    code = models.CharField(
        _('Код инструмента'),
        max_length=30,
        blank=True, null=True,
    )
    name = models.CharField(
        _('Название'),
        max_length=2000,
        blank=False, null=False,
        default='',
    )
    inventory_number = models.CharField(
        _('Инвентарный номер'),
        max_length=255,
        blank=False, null=False,
        default='',
    )
    equipment_group = models.ForeignKey(
        EquipmentGroup,
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name=_('Группа'),
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Компания'),
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'equipment'
        verbose_name = 'Инструмент'
        verbose_name_plural = 'Инструменты'

    def __str__(self):
        return self.name


class Workplace(models.Model):
    """
        Рабочее место
    """
    code = models.CharField(
        _('Код рабочего места'),
        max_length=30,
        blank=True, null=True,
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Должность'),
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Подразделение'),
    )
    equipment = models.ManyToManyField(
        Equipment,
        verbose_name=_('Инструмент'),
    )
    instruction_required = models.BooleanField(
        _('Необходимость проходить инструктаж по электробезопасности'),
        blank=False, null=False,
        default=True,
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'workplace'
        verbose_name = 'Рабочее место'
        verbose_name_plural = 'Рабочие места'

    def __str__(self):
        return '{} in {} ({})'.format(self.position.name, self.department.name, self.department.company.name)

    def position_name(self):
        return self.position.name

    def department_name(self):
        return self.department.name

    def company_name(self):
        return self.department.company.name


class Employee(models.Model):
    """
        Сотрудник
    """
    GENDER_CHOICES = (
        ('m', 'мужчина'),
        ('f', 'женщина'),
    )

    last_name = models.CharField(
        _('Фамилия'),
        max_length=255,
        blank=False, null=False,
        default='',
    )
    first_name = models.CharField(
        _('Имя'),
        max_length=255,
        blank=False, null=False,
        default='',
    )
    middle_name = models.CharField(
        _('Отчество'),
        max_length=255,
        blank=True, null=True,
    )
    address = models.CharField(
        _('Адрес проживания'),
        max_length=2000,
        blank=True, null=True,
    )
    birth_date = models.DateField(
        _('Дата рождения'),
        blank=False, null=False,
        default=datetime.date.today,
    )
    gender = models.CharField(
        _('Пол'),
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True, null=True,
    )
    disability = models.BooleanField(
        _('Инвалидность'),
        blank=True, null=True,
    )
    employment_date = models.DateField(
        _('Дата приема на работу'),
        blank=False, null=False,
        default=datetime.date.today,
    )
    pers_number = models.CharField(
        _('Табельный номер'),
        max_length=255,
        blank=True, null=True,
    )
    avatar = ThumbnailerImageField(
        _('Аватарка'),
        upload_to ='avatars/',
        blank=True, null=True,
        resize_source=dict(size=(128, 128), sharpen=True),
    )
    insurance_number = models.CharField(
        _('Страховой номер (СНИЛС)'),
        max_length=255,
        blank=True, null=True,
    )
    workplace = models.ManyToManyField(
        Workplace,
        verbose_name=_('Рабочее место'),
        related_name='employees',
    )
    fire_date = models.DateField(
        _('Дата увольнения'),
        blank=True, null=True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Компания'),
    )

    class Meta:
        db_table = 'employee'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return '{} {} {}'.format(self.last_name, self.first_name, self.middle_name if self.middle_name else '')

    def company_name(self):
        return self.company.name


class WorkingConditionClass(models.Model):
    """
        Класс условий труда
    """
    name = models.CharField(
        _('Класс'),
        max_length=255,
        blank=False, null=False,
        default='',
    )

    class Meta:
        db_table = 'working_condition_class'
        verbose_name = _('Класс условий труда')
        verbose_name_plural = _('Классы условий труда')


class HarmfulFactor(models.Model):
    """
        Вредный фактор
    """
    code = models.CharField(
        _('Номер'),
        max_length=30,
        blank=True, null=True,
    )
    name = models.CharField(
        _('Наименование'),
        max_length=2000,
        blank=False, null=False,
        default='',
    )
    inspection_frequency = models.CharField(
        _('Периодичность осмотра'),
        max_length=50,
        choices=INSPECTION_FREQUENCY,
        blank=False, null=False,
        default='10 1t/1y',
    )

    class Meta:
        db_table = 'harmful_factor'
        verbose_name = _('Вредный фактор')
        verbose_name_plural = _('Вредные факторы')


class WorkType(models.Model):
    """
        Вид работ и профессий
    """
    code = models.CharField(
        _('Номер'),
        max_length=30,
        blank=True, null=True,
    )
    name = models.CharField(
        _('Наименование'),
        max_length=2000,
        blank=False, null=False,
        default='',
    )
    inspection_frequency = models.CharField(
        _('Периодичность осмотра'),
        max_length=50,
        choices=INSPECTION_FREQUENCY,
        blank=False, null=False,
        default='10 1t/1y',
    )

    class Meta:
        db_table = 'work_type'
        verbose_name = _('Вид работ и профессий')
        verbose_name_plural = _('Виды работ и профессий')


class HarmfulSubstance(models.Model):
    """
        Вредные вещества
    """
    category = models.CharField(
        _('Категория'),
        max_length=50,
        choices=CATEGORY,
        blank=False, null=False,
        default='chemical',
    )
    name = models.CharField(
        _('Наименование'),
        max_length=2000,
        blank=False, null=False,
        default='',
    )

    class Meta:
        db_table = 'harmful_substance'
        verbose_name = _('Вредное вещество')
        verbose_name_plural = _('Вредные вещества')


class AssessmentCard(models.Model):
    """
        Карта СОУТ (Специальная оценка условий труда)
    """
    card_number = models.CharField(
        _('Номер карты'),
        max_length=50,
        blank=False, null=False,
        default='',
    )
    workplace = models.ForeignKey(
        Workplace,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Рабочее место'),
    )
    working_condition_class = models.ForeignKey(
        WorkingConditionClass,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Класс условий труда'),
    )
    signing_date = models.DateField(
        _('Дата подписания карты'),
        blank=True, null=True,
    )
    next_assessment_date = models.DateField(
        _('Дата следующей оценки'),
        blank=True, null=True,
    )
    harmful_factor = models.ManyToManyField(
        HarmfulFactor,
        verbose_name=_('Вредный фактор'),
    )
    work_type = models.ManyToManyField(
        WorkType,
        verbose_name=_('Вид работ'),
    )
    harmful_substance = models.ManyToManyField(
        HarmfulSubstance,
        verbose_name=_('Вредное вещество'),
    )
    increased_pay = models.BooleanField(
        _('Повышенная оплата труда'),
        blank=False, null=False,
        default=False,
    )
    extra_vacation = models.BooleanField(
        _('Дополнительный отпуск'),
        blank=False, null=False,
        default=False,
    )
    reduced_working_hours = models.BooleanField(
        _('Сокращенная продолжительность рабочего дня'),
        blank=False, null=False,
        default=False,
    )
    milk = models.BooleanField(
        _('Молоко'),
        blank=False, null=False,
        default=False,
    )
    therapeutic_nutrition = models.BooleanField(
        _('Лечебно-профилактическое питание'),
        blank=False, null=False,
        default=False,
    )
    early_retirement = models.BooleanField(
        _('Право на досрочное назначение страховой пенсии'),
        blank=False, null=False,
        default=False,
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'assessment_card'
        verbose_name = 'Карта СОУТ'
        verbose_name_plural = 'Карты СОУТ'

    def __str__(self):
        return '{}'.format(self.card_number)


class Ppe(models.Model):
    """
        СИЗ (Средство индивидуальной защиты)
    """
    name = models.CharField(
        _('Наименование'),
        max_length=255,
        blank=False, null=False,
        default='',
    )
    description = models.CharField(
        _('Описание'),
        max_length=2000,
        blank=True, null=True,
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'ppe'


class PpeStandard(models.Model):
    """
        Норма выдачи СИЗ
    """
    decree = models.CharField(
        _('Основание'),
        max_length=2000,
        blank=False, null=False,
        default='',
    )
    paragraph = models.CharField(
        _('Номер пункта'),
        max_length=30,
        blank=True, null=True,
    )
    ppe = models.ForeignKey(
        Ppe,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('СИЗ'),
    )
    item_count = models.PositiveIntegerField(
        _('Количество'),
        blank=False, null=False,
        default=0,
    )

    class Meta:
        db_table = 'ppe_standard'


class EventType(models.Model):
    """
        Вид мероприятия
    """
    name = models.CharField(
        _('Наименование'),
        max_length=255,
        blank=False, null=False,
        default='',
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

    class Meta:
        db_table = 'event_type'
        verbose_name = _('Вид мероприятия')
        verbose_name_plural = _('Виды мероприятий')

    def __str__(self):
        return self.name


class Commission(models.Model):
    """
        Комиссия
    """
    num = models.PositiveIntegerField(
        _('№ п/п'),
        blank=False, null=False,
        default=1,
    )
    name = models.CharField(
        _('Наименование'),
        max_length=2000,
        blank=False, null=False,
        default='',
    )
    decree = models.CharField(
        _('Приказ'),
        max_length=255,
        blank=True, null=True,
    )
    decree_date = models.DateField(
        _('Дата приказа'),
        blank=True, null=True,
    )
    employee = models.ManyToManyField(
        Employee,
        verbose_name=_('Сотрудник'),
        through='CommissionEmployee',
        through_fields=['commission', 'employee',],    
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Компания'),
    )
    document_template = models.ForeignKey(
        'documents.DocumentTemplate',
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name=_('Шаблон'),
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'commission'
        verbose_name = _('Комиссия')
        verbose_name_plural = _('Комиссии')

    def __str__(self):
        return '{}'.format(self.name)


class CommissionEmployee(models.Model):
    """
        Комиссия - Сотрудник
    """
    MEMBER_STATUSES = (
        (1, 'Председатель'),
        (2, 'Секретарь'),
        (3, 'Член'),
    )
    commission = models.ForeignKey(
        'Commission',
        to_field='id',
        on_delete=models.PROTECT,
        verbose_name=_('Комиссия'),
        blank=False, null=False,
        db_column='commission_id',
    )
    employee = models.ForeignKey(
        'Employee',
        to_field='id',
        on_delete=models.PROTECT,
        verbose_name=_('Сотрудник'),
        blank=False, null=False,
        db_column='employee_id',
    )
    member_status = models.PositiveIntegerField(
        _('Статус участника'),
        choices=MEMBER_STATUSES,
        blank=False, null=False,
        default=3,
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'commission_employee'
        verbose_name = _('Комиссия - Сотрудник')
        verbose_name_plural = _('Комиссии - Сотрудники')

    def __str__(self):
        return '{} - {}'.format(self.commission.name, self.employee.last_name)


class Event(Entity):
    """
        Мероприятие
    """
    FREQUENCY = (
        ('1/t', 'Единоразово'),
        ('1/m', 'Раз в месяц'),
        ('1/q', 'Раз в квартал'),
        ('2/y', 'Два раза в год'),
        ('1/y', 'Раз в год'),
        ('1/2y', 'Раз в два года'),
        ('1/w', 'Раз в неделю'),
    )
    event_type = models.ForeignKey(
        EventType,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Вид мероприятия'),
        default=1,
    )
    name = models.CharField(
        _('Наименование'),
        max_length=2000,
        blank=False, null=False,
        default='',
    )
    event_date = models.DateField(
        _('Дата мероприятия'),
        blank=False, null=False,
        default=datetime.date.today,
    )
    frequency = models.CharField(
        _('Периодичность'),
        max_length=20,
        choices=FREQUENCY,
        blank=False, null=False,
        default='1/t',
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Компания'),
    )
    commission = models.ForeignKey(
        Commission,
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name=_('Комиссия'),
    )
    previous = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name=_('Предыдущее'),
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'event'
        verbose_name = _('Мероприятие')
        verbose_name_plural = _('Мероприятия')

    def __str__(self):
        return self.name


class EventEmployee(Entity):
    """
        Мероприятие - Сотрудник
    """
    event_instance = models.ForeignKey(
        Event,
        to_field='entity_ptr',
        on_delete=models.PROTECT,
        verbose_name=_('Мероприятие'),
        blank=False, null=False,
        db_column='event_id',
        related_name='employees',
    )
    employee = models.ForeignKey(
        Employee,
        to_field='id',
        on_delete=models.PROTECT,
        verbose_name=_('Сотрудник'),
        blank=False, null=False,
        db_column='employee_id',
    )
    event_date = models.DateField(
        _('Дата мероприятия'),
        blank=True, null=True,
    )
    certificate = models.CharField(
        _('Сертификат'),
        max_length=255,
        blank=True, null=True,
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'event_employee'
        verbose_name = _('Мероприятие - Сотрудник')
        verbose_name_plural = _('Мероприятия - Сотрудники')

    def __str__(self):
        return '{} - {}'.format(self.event.name, self.employee.last_name)


class EventDocumentTemplate(models.Model):
    """
        Мероприятие - Документ
    """
    APPLY_TO = (
        ('event', 'Мероприятие'),
        ('commission', 'Комиссия'),
        ('employee', 'Участник'),
    )
    event = models.ForeignKey(
        Event,
        to_field='entity_ptr',
        on_delete=models.PROTECT,
        verbose_name=_('Мероприятие'),
        blank=False, null=False,
        db_column='event_id',
        related_name='event_to_doc_template',
    )
    document_template = models.ForeignKey(
        'documents.DocumentTemplate',
        to_field='entity_ptr',
        on_delete=models.PROTECT,
        verbose_name=_('Документ'),
        blank=False, null=False,
        db_column='document_template_id',
    )
    apply_to = models.CharField(
        _('Применить'),
        max_length=20,
        choices=APPLY_TO,
        blank=False, null=False,
        default='event',
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'event_document_template'
        verbose_name = _('Мероприятие - Документ')
        verbose_name_plural = _('Мероприятия - Документы')

    def __str__(self):
        return '{} - {}'.format(self.event.name, self.document_template.name)