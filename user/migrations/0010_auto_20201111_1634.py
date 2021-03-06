# Generated by Django 3.1.3 on 2020-11-11 21:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20201111_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2022, 11, 11, 16, 34, 3, 516084), help_text='Date upon which ATM card expires. Defaults to two years from date of issue'),
        ),
    ]
