# Generated by Django 2.1.5 on 2019-05-03 15:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190503_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singletest',
            name='operating_mode',
            field=models.CharField(choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior')], default='FR', max_length=2),
        ),
        migrations.AlterField(
            model_name='testscenario',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 3, 16, 52, 26, 901092)),
        ),
    ]