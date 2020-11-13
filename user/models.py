from django.db import models
from django.contrib.auth.models import User
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
                                   help_text="Status of ATM Card. Card can either be Open or Closed.", )

    owner_id = models.ForeignKey(User, on_delete=models.PROTECT, help_text="Card holder's account.", )

    # Methods
    def __str__(self):
        string = ("Date of Issue: %s\nExpiry Date: %s\nCard Status: %s\n" %
                  (self.date_of_issue, self.expiry_date, self.card_status))
        return string

    # Properties
    @property
    def is_expired(self):
        if self.expiry_date and datetime.now().date() > self.expiry_date:
            return True
        return False


class Customer(models.Model):
    # Fields:
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE,
                                help_text="The user's login name.", )

    pin_regex = RegexValidator(regex=r'^\d{1,10}$',
                               message="PIN number must be 4 digits.")
    pin_number = models.CharField(max_length=4, validators=[pin_regex],
                                  help_text="A four digit PIN number.", blank=False, )

    address = models.CharField(max_length=300, help_text="User's address.", blank=False)

    # todo: better address validation if there is remaining time
    balance = models.PositiveIntegerField(default=0, help_text="User's balance.", blank=False, )

    # Regex validator used to verify phone number
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: "
                                         "'+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False,
                                    help_text="The user's phone number.")

    # Methods:
    def __str__(self):
        string = ("Username: %s\nPIN: %s\nAddress: %s\nBalance: %s\nPhone Number: %s\n" %
                  (self.user, self.pin_number, self.address, self.balance, self.phone_number))
        return string

    # todo: withdraw money

    # todo: deposit money

    
