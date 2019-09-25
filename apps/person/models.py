from django.db import models
import datetime


class DepartmentType(models.Model):
    """
        Тип подразделения
    """
    name = models.CharField(
        _('Название'),
        max_length=255,
        blank=False, null=False,
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
    )
    name = models.CharField(
        _('Название'),
        max_length=2000,
        blank=False, null=False,
    )
    type = models.ForeignKey(
        _('Тип подразделения'),
        DepartmentType,
        on_delete=models.PROTECT,
        blank=False, null=False,
    )
    parent = models.ForeignKey(
        _('Вышестоящее подразделение'),
        'self',
        on_delete=models.PROTECT,
        blank=True, null=True,
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
    )
    name = models.CharField(
        _('Название'),
        max_length=2000,
        blank=False, null=False,
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
    )
    name = models.CharField(
        _('Название'),
        max_length=2000,
        blank=False, null=False,
    )
    inventory_number = models.CharField(
        _('Инвентарный номер'),
        max_length=255,
        blank=False, null=False,
    )
    equipment_group = models.ForeignKey(
        _('Группа'),
        EquipmentGroup,
        on_delete=models.PROTECT,
        blank=True, null=True,
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
    )
    name = models.CharField(
        _('Название'),
        max_length=2000,
        blank=False, null=False,
    )
    position = models.ForeignKey(
        _('Должность'),
        Position,
        on_delete=models.PROTECT,
        blank=False, null=False,
    )
    department = models.ForeignKey(
        _('Подразделение'),
        Department,
        on_delete=models.PROTECT,
        blank=False, null=False,
    )
    equipment = models.ManyToManyField(
        _('Инструмент'),
        Equipment,
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
    )
    first_name = models.CharField(
        _('Имя'),
        max_length=255,
        blank=False, null=False,
    )
    middle_name = models.CharField(
        _('Отчество'),
        max_length=255,
        blank=False, null=False,
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
    )
    insurance_number = models.CharField(
        _('Страховой номер (СНИЛС)'),
        max_length=255,
        blank=False, null=False,
    )
    workplace = models.ManyToManyField(
        _('Рабочее место'),
        Workplace,
    )
    fire_date = models.DateField(
        _('Дата увольнения'),
        blank=True, null=True,
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
    )
    description = models.CharField(
        _('Примечание'),
        max_length=2000,
        blank=True, null=True,
    )

    class Meta:
        db_table = 'certificate'


class HarmfulFactor(models.Model):
    """
        Вредный фактор
    """
    code = models.CharField(
        _('Номер'),
        blank=False, null=False,
    )
    name = models.CharField(
        _('Номер сертификата'),
        max_length=2000,
        blank=False, null=False,
    )
    inspection_frequency = models.CharField(
        _('Периодичность осмотра'),
        max_length=50,
        blank=False, null=False,
    )
    inspection_frequency_i = models.PositiveIntegerField(
        _('Периодичность осмотра'),
        blank=False, null=False,
    )

    class Meta:
        db_table = 'harmful_factor'


class AssessmentCard(models.Model):
    """
        Карта СОУТ (Специальная оценка условий труда)
    """
    card_number = models.CharField(
        _('Номер карты'),
        blank=False, null=False,
    )
    workplace = models.ForeignKey(
        _('Рабочее место'),
        Workplace,
        on_delete=models.PROTECT,
        blank=False, null=False,
    )
    working_condition_class = models.ForeignKey(
        _('Класс условий труда'),
        WorkingConditionClass,
        on_delete=models.PROTECT,
        blank=False, null=False,
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
        _('Вредный фактор'),
        HarmfulFactor,
    )

    class Meta:
        db_table = 'assessment_card'
