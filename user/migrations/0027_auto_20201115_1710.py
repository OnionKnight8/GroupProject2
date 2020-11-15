# Generated by Django 3.1.3 on 2020-11-15 22:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0026_auto_20201115_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_amount',
            field=models.PositiveIntegerField(default=25, help_text='Amount of money involved in transaction.'),
        ),
        migrations.AlterField(
            model_name='atmmachine',
            name='last_refill_date',
            field=models.DateField(default=datetime.datetime(2020, 11, 15, 17, 10, 51, 703496), help_text='Date upon which machine was last serviced.'),
        ),
        migrations.AlterField(
            model_name='atmmachine',
            name='next_refill_date',
            field=models.DateField(default=datetime.datetime(2020, 11, 29, 17, 10, 51, 703496), help_text='Date upon which machine should be serviced next. Defaults to two weeks from date of last refill, but can be changed.'),
        ),
        migrations.AlterField(
            model_name='card',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2022, 11, 15, 17, 10, 51, 702495), help_text='Date upon which ATM card expires. Defaults to two years from date of issue'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_status',
            field=models.CharField(choices=[('CO', 'Completed'), ('CA', 'Canceled')], default='CO', help_text='Status of transaction.', max_length=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transfer_id',
            field=models.ForeignKey(blank=True, default=None, help_text='User in which money is transferred to. Only used in a transfer.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL),
        ),
    ]
