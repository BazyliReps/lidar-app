# Generated by Django 2.1.5 on 2019-05-03 16:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20190503_1719'),
    ]

    operations = [
        migrations.RenameField(
            model_name='singletest',
            old_name='TestBoard',
            new_name='board',
        ),
        migrations.AlterField(
            model_name='singletest',
            name='name',
            field=models.CharField(max_length=200, verbose_name='opis'),
        ),
        migrations.AlterField(
            model_name='singletest',
            name='operating_mode',
            field=models.CharField(choices=[('const', 'ciągły'), ('1', '1'), ('2', '1/2'), ('4', '1/4'), ('8', '1/8'), ('16', '1/16'), ('32', '1/32')], default='1', max_length=2, verbose_name='tryb pracy'),
        ),
        migrations.AlterField(
            model_name='testscenario',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 3, 17, 49, 11, 367289)),
        ),
    ]