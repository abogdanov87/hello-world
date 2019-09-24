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
    name = models.CharField(
        _('Название'),
        max_length=2000,
        blank=False, null=False,
    )
    type = models.ForeignKey(
        _('Тип подразделения'),
        DepartmentType,
        on_delete=models.CASCADE,
        blank=False, null=False,
    )
    parent = models.ForeignKey(
        _('Вышестоящее подразделение'),
        'self',
        on_delete=models.CASCADE,
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
    department = models.ForeignKey(
        _('Подразделение'),
        Department,
        on_delete=models.CASCADE,
        blank=False, null=False,
    )
    position = models.ForeignKey(
        _('Должность'),
        Position,
        on_delete=models.CASCADE,
        blank=False, null=False,
    )
    fire_date = models.DateField(
        _('Дата увольнения'),
        blank=True, null=True,
    )

    class Meta:
        db_table = 'employee'


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
        on_delete=models.CASCADE,
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
    name = models.CharField(
        _('Название'),
        max_length=2000,
        blank=False, null=False,
    )
    position = models.ForeignKey(
        _('Должность'),
        Position,
        on_delete=models.CASCADE,
        blank=False, null=False,
    )
    department = models.ForeignKey(
        _('Подразделение'),
        Department,
        on_delete=models.CASCADE,
        blank=False, null=False,
    )
    equipment = models.ManyToManyField(
        _('Инструмент'),
        Equipment,
    )
    instruction_required = models.BooleanField(
        _('Необходимость проходить инструктаж по электробезопасности'),
        blank=False, null=False,
        default=False,
    )
    active = models.BooleanField(
        _('Статус активности'),
        blank=False, null=False,
        default=True,
    )

    class Meta:
        db_table = 'workplace'


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
