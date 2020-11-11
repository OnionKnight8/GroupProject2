# Generated by Django 3.1.3 on 2020-11-11 21:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0005_auto_20201110_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2022, 11, 11, 16, 2, 1, 483151), help_text='Date upon which ATM card expires. Defaults to two years from date of issue'),
        ),
        migrations.AlterField(
            model_name='card',
            name='owner_id',
            field=models.ForeignKey(help_text='Account number of card holder.', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
