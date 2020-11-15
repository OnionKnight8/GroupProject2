# Generated by Django 3.1.3 on 2020-11-15 22:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0029_auto_20201115_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atmmachine',
            name='last_refill_date',
            field=models.DateField(default=datetime.datetime(2020, 11, 15, 17, 39, 28, 805257), help_text='Date upon which machine was last serviced.'),
        ),
        migrations.AlterField(
            model_name='atmmachine',
            name='next_refill_date',
            field=models.DateField(default=datetime.datetime(2020, 11, 29, 17, 39, 28, 805257), help_text='Date upon which machine should be serviced next. Defaults to two weeks from date of last refill, but can be changed.'),
        ),
        migrations.AlterField(
            model_name='card',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2022, 11, 15, 17, 39, 28, 805257), help_text='Date upon which ATM card expires. Defaults to two years from date of issue'),
        ),
    ]