# Generated by Django 3.1.3 on 2020-11-15 18:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_auto_20201115_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atmmachine',
            name='last_refill_date',
            field=models.DateField(default=datetime.datetime(2020, 11, 15, 13, 49, 27, 509106), help_text='Date upon which machine was last serviced.'),
        ),
        migrations.AlterField(
            model_name='atmmachine',
            name='next_refill_date',
            field=models.DateField(default=datetime.datetime(2020, 11, 29, 13, 49, 27, 509106), help_text='Date upon which machine should be serviced next. Defaults to two weeks from date of last refill, but can be changed.'),
        ),
        migrations.AlterField(
            model_name='card',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2022, 11, 15, 13, 49, 27, 508107), help_text='Date upon which ATM card expires. Defaults to two years from date of issue'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_status',
            field=models.CharField(choices=[('CO', 'Completed'), ('CA', 'Canceled'), ('PE', 'Pending')], default='PE', help_text='Status of transaction.', max_length=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('DE', 'Deposit'), ('WI', 'Withdrawal'), ('TR', 'Transfer')], default='DE', help_text='The type of transaction to be processed.', max_length=10),
        ),
    ]
