# Generated by Django 3.1.3 on 2020-11-10 20:02

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20201110_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2022, 11, 10, 15, 2, 4, 853057), help_text='Date upon which ATM card expires. Defaults to two years from date of issue'),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(help_text="User's address. Please use format 1234 Example Street, Apartment Number, City, State ZIP", max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(help_text="The account owner's phone number.", max_length=15, validators=[django.core.validators.RegexValidator('^\\d{10,15}$', 'Phone number cannot contain text or be less than 10 Digits!', 'Invalid Input')]),
        ),
    ]
