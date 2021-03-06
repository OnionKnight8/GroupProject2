# Generated by Django 3.1.3 on 2020-11-13 22:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_auto_20201113_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2022, 11, 13, 17, 12, 21, 386990), help_text='Date upon which ATM card expires. Defaults to two years from date of issue'),
        ),
    ]
