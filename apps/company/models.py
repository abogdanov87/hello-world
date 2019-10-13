from django.db import models
import datetime

from django.utils.translation import gettext_lazy as _


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
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'company'
        verbose_name = _('Компания')
        verbose_name_plural = _('Компании')


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
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'department_type'


class Department(models.Model):
    """
        Подразделение
    """
    code = models.CharField(
        _('Код подразделения'),
        max_length=30,
        blank=False, null=False,
        default='',
    )
    name = models.CharField(
        _('Название'),
        max_length=2000,
        blank=False, null=False,
        default='',
    )
    type = models.ForeignKey(
        DepartmentType,
        on_delete=models.PROTECT,
        blank=False, null=False,
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
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'department'


class Position(models.Model):
    """
        Должность
    """
    code = models.CharField(
        _('Код должности'),
        max_length=30,
        blank=False, null=False,
        default='',
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
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'position'


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


class Equipment(models.Model):
    """
        Инструмент
    """
    code = models.CharField(
        _('Код инструмента'),
        max_length=30,
        blank=False, null=False,
        default='',
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


class Workplace(models.Model):
    """
        Рабочее место
    """
    code = models.CharField(
        _('Код рабочего места'),
        max_length=30,
        blank=False, null=False,
        default='',
    )
    name = models.CharField(
        _('Название'),
        max_length=2000,
        blank=False, null=False,
        default='',
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


class Employee(models.Model):
    """
        Сотрудник
    """
    SEX_CHOICES = (
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
        blank=False, null=False,
        default='',
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
    sex = models.CharField(
        _('Пол'),
        max_length=1,
        choices=SEX_CHOICES,
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
        blank=False, null=False,
        default='',
    )
    insurance_number = models.CharField(
        _('Страховой номер (СНИЛС)'),
        max_length=255,
        blank=False, null=False,
        default='',
    )
    workplace = models.ManyToManyField(
        Workplace,
        verbose_name=_('Рабочее место'),
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


class Certificate(models.Model):
    """
        Сертификат
    """
    num = models.PositiveIntegerField(
        _('Номер п.п'),
        blank=False, null=False,
        default=1,
    )
    certificate_number = models.CharField(
        _('Номер сертификата'),
        max_length=255,
        blank=False, null=False,
        default='',
    )
    description = models.CharField(
        _('Примечание'),
        max_length=2000,
        blank=True, null=True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Компания'),
    )

    class Meta:
        db_table = 'certificate'


class HarmfulFactor(models.Model):
    """
        Вредный фактор
    """
    code = models.CharField(
        _('Номер'),
        max_length=30,
        blank=False, null=False,
        default='',
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
        blank=False, null=False,
        default='',
    )

    class Meta:
        db_table = 'harmful_factor'


class WorkType(models.Model):
    """
        Вид работ и профессий
    """
    code = models.CharField(
        _('Номер'),
        max_length=30,
        blank=False, null=False,
        default='',
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
        blank=False, null=False,
        default='',
    )

    class Meta:
        db_table = 'work_type'


class MedicalType(models.Model):
    """
        Вид мед. осмотра
    """
    name = models.CharField(
        _('Наименование'),
        max_length=2000,
        blank=False, null=False,
        default='',
    )

    class Meta:
        db_table = 'medical_type'


class PsychiatricType(models.Model):
    """
        Вид психиатрического освидетельствования
    """
    name = models.CharField(
        _('Наименование'),
        max_length=2000,
        blank=False, null=False,
        default='',
    )

    class Meta:
        db_table = 'psychiatric_type'


class AssessmentCard(models.Model):
    """
        Карта СОУТ (Специальная оценка условий труда)
    """
    ANSWERS = (
        (0, 'Нет'),
        (1, 'Да'),
    )

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
    medical_inspection = models.PositiveIntegerField(
        _('Проведение медицинских осмотров'),
        choices=ANSWERS,
        blank=False, null=False,
        default=1,
    )
    increased_pay = models.PositiveIntegerField(
        _('Повышенная оплата труда'),
        choices=ANSWERS,
        blank=False, null=False,
        default=0,
    )
    extra_vacation = models.PositiveIntegerField(
        _('Дополнительный отпуск'),
        choices=ANSWERS,
        blank=False, null=False,
        default=0,
    )
    reduced_working_hours = models.PositiveIntegerField(
        _('Сокращенная продолжительность рабочего дня'),
        choices=ANSWERS,
        blank=False, null=False,
        default=0,
    )
    milk = models.PositiveIntegerField(
        _('Молоко'),
        choices=ANSWERS,
        blank=False, null=False,
        default=0,
    )
    therapeutic_nutrition = models.PositiveIntegerField(
        _('Лечебно-профилактическое питание'),
        choices=ANSWERS,
        blank=False, null=False,
        default=0,
    )
    early_retirement = models.PositiveIntegerField(
        _('Право на досрочное назначение страховой пенсии'),
        choices=ANSWERS,
        blank=False, null=False,
        default=0,
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'assessment_card'


class EducationType(models.Model):
    """
        Вид обучения (аттестации)
    """
    name = models.CharField(
        _('Наименование'),
        max_length=2000,
        blank=False, null=False,
        default='',
    )
    frequency = models.CharField(
        _('Периодичность'),
        max_length=50,
        blank=False, null=False,
        default='',
    )

    class Meta:
        db_table = 'education_type'


class CertificationType(models.Model):
    """
        Виды аттестаций
    """
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Сотрудник'),
    )
    education_date = models.DateField(
        _('Дата обучения'),
        blank=False, null=False,
        default=datetime.date.today,
    )
    id_number = models.CharField(
        _('Номер удостоверения'),
        max_length=50,
        blank=False, null=False,
        default='',
    )
    education_type = models.ForeignKey(
        EducationType,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Вид обучения'),
    )
    next_education_date = models.DateField(
        _('Контрольная дата очередной аттестации'),
        blank=False, null=False,
        default=datetime.date.today,
    )
    days_to_education = models.PositiveIntegerField(
        _('Дней до очередной аттестации'),
        blank=True, null=True,
    )

    class Meta:
        db_table = 'certification_type'


class MemberStatus(models.Model):
    """
        Статус участника
    """
    name = models.CharField(
        _('Наименование'),
        max_length=2000,
        blank=False, null=False,
        default='',
    )

    class Meta:
        db_table = 'member_status'


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
    member_status = models.ForeignKey(
        MemberStatus,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Статус участника'),
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name=_('Сотрудник'),
    )

    class Meta:
        db_table = 'commission'
