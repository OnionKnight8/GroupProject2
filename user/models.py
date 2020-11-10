from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime, timedelta
import secrets


class Card(models.Model):
    # Fields
    date_of_issue = models.DateField(auto_now=True, help_text="Date that ATM Card was Issued.", )
    expiry_date = models.DateField(default=datetime.now() + timedelta(days=730),
                                   help_text="Date upon which ATM card expires. Defaults to two years from date of "
                                             "issue", )

    # ATM Card Status Options
    OPEN = 'OP'
    CLOSED = 'CL'
    CARD_STATUS_CHOICES = (
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    )
    card_status = models.CharField(max_length=6, choices=CARD_STATUS_CHOICES, default=OPEN,
                                   help_text="Status of ATM Card. Card can Either be Open or Closed.", )

    owner_id = models.ForeignKey('User', on_delete=models.PROTECT, help_text="Account number of card holder.", )

    # Methods
    def __str__(self):
        string = ("Date of Issue: %s\nExpiry Date: %s\nCard Status: %s\n" %
                  (self.date_of_issue, self.expiry_date, self.card_status))
        return string


class User(models.Model):
    # Fields
    account_number = models.AutoField(primary_key=True, help_text="Auto generated account number. "
                                                                  "Cannot be changed!", )
    pin = models.CharField(max_length=4, validators=[RegexValidator(r'^\d{1,4}$',
                                                                    'PIN Must be 4 Digits!', 'Invalid Input')],
                           help_text="A four-digit PIN number", )
    # account_name = models.CharField(max_length=50, unique=True, help_text="A user name.",)
    address = models.CharField(blank=False, max_length=200, help_text="User's address. Please use format "
                                                                      "1234 Example Street, Apartment Number, City, "
                                                                      "State ZIP", )
    balance = models.IntegerField(default=0, editable=False, help_text="The account's current balance.", )
    phone_number = models.CharField(max_length=15, blank=False,
                                    validators=[RegexValidator(r'^\d{10,15}$',
                                                               'Phone number cannot contain text or be less '
                                                               'than 10 Digits!',
                                                               'Invalid Input')],
                                    help_text="The account owner's phone number.", )

    # Methods
    def __str__(self):
        string = ("""Account Number: %s\nPIN: %s\n
        Address: %s\nBalance: %s\nPhone Number: %s\n""" %
                  (self.account_number, self.pin,
                   self.address, self.balance, self.phone_number))
        return string
