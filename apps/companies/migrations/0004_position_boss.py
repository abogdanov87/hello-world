# Generated by Django 2.2.6 on 2020-04-03 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_auto_20200403_0446'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='boss',
            field=models.BooleanField(default=False, verbose_name='Руководящая позиция'),
        ),
    ]
