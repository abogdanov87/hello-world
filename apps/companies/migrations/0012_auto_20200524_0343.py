# Generated by Django 2.2.6 on 2020-05-24 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0011_auto_20200518_0826'),
    ]

    operations = [
        migrations.CreateModel(
            name='HarmfulSubstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=2000, verbose_name='Наименование')),
            ],
            options={
                'db_table': 'harmful_substance',
            },
        ),
        migrations.RemoveField(
            model_name='certificate',
            name='company',
        ),
        migrations.RemoveField(
            model_name='certificationtype',
            name='education_type',
        ),
        migrations.RemoveField(
            model_name='certificationtype',
            name='employee',
        ),
        migrations.DeleteModel(
            name='MedicalType',
        ),
        migrations.DeleteModel(
            name='MemberStatus',
        ),
        migrations.DeleteModel(
            name='PsychiatricType',
        ),
        migrations.AlterModelOptions(
            name='assessmentcard',
            options={'verbose_name': 'Карта СОУТ', 'verbose_name_plural': 'Карты СОУТ'},
        ),
        migrations.RemoveField(
            model_name='assessmentcard',
            name='medical_inspection',
        ),
        migrations.AlterField(
            model_name='assessmentcard',
            name='early_retirement',
            field=models.BooleanField(default=False, verbose_name='Право на досрочное назначение страховой пенсии'),
        ),
        migrations.AlterField(
            model_name='assessmentcard',
            name='extra_vacation',
            field=models.BooleanField(default=False, verbose_name='Дополнительный отпуск'),
        ),
        migrations.AlterField(
            model_name='assessmentcard',
            name='increased_pay',
            field=models.BooleanField(default=False, verbose_name='Повышенная оплата труда'),
        ),
        migrations.AlterField(
            model_name='assessmentcard',
            name='milk',
            field=models.BooleanField(default=False, verbose_name='Молоко'),
        ),
        migrations.AlterField(
            model_name='assessmentcard',
            name='reduced_working_hours',
            field=models.BooleanField(default=False, verbose_name='Сокращенная продолжительность рабочего дня'),
        ),
        migrations.AlterField(
            model_name='assessmentcard',
            name='therapeutic_nutrition',
            field=models.BooleanField(default=False, verbose_name='Лечебно-профилактическое питание'),
        ),
        migrations.DeleteModel(
            name='Certificate',
        ),
        migrations.DeleteModel(
            name='CertificationType',
        ),
        migrations.DeleteModel(
            name='EducationType',
        ),
        migrations.AddField(
            model_name='assessmentcard',
            name='harmful_substance',
            field=models.ManyToManyField(to='companies.HarmfulSubstance', verbose_name='Вредное вещество'),
        ),
    ]
