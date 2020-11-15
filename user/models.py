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
    PENDING = 'PE'
    CARD_STATUS_CHOICES = (
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
        (PENDING, 'Pending'),
    )
    card_status = models.CharField(max_length=6, choices=CARD_STATUS_CHOICES, default=PENDING,
                                   help_text="Status of ATM Card. Card can either be Open or Closed. "
                                             "Pending means that card has been submitted by a user, but not yet "
                                             "approved by an admin.", )

    owner_id = models.ForeignKey(User, on_delete=models.PROTECT, help_text="Card holder's account.", )

    # Methods
    def __str__(self):
        string = ("Owner: %s\nDate of Issue: %s\nExpiry Date: %s\nCard Status: %s\n" %
                  (self.owner_id, self.date_of_issue, self.expiry_date, self.card_status))
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


class ATMMachine(models.Model):
    # Fields
    address = models.CharField(max_length=300, help_text="ATM Machine's Address.", blank=False)
    # todo: better address validation if there is remaining time

    # ATM Machine Status Choices
    ACTIVE = 'AC'
    INACTIVE = 'IN'
    MACHINE_STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )
    machine_status = models.CharField(max_length=8, choices=MACHINE_STATUS_CHOICES, default=ACTIVE,
                                      help_text="Status of ATM Machine. "
                                                "Mark Active if machine is functional, otherwise mark inactive.",)

    last_refill_date = models.DateField(default=datetime.now(), blank=False,
                                        help_text="Date upon which machine was last serviced.",)
    next_refill_date = models.DateField(default=datetime.now() + timedelta(days=14), blank=False,
                                        help_text="Date upon which machine should be serviced next. "
                                                  "Defaults to two weeks from date of last refill, "
                                                  "but can be changed.",)

    min_balance_inquiry = models.PositiveIntegerField(default=25, blank=False,
                                                      help_text="The minimum balance enquiry. There is usually no "
                                                                "reason to change this.",)
    current_balance = models.PositiveIntegerField(default=0, help_text="Machine's current balance.", blank=False, )

    # Methods
    def __str__(self):
        string = ("Address: %s\nStatus: %s\nLast Refill: %s\nNext Refill: %s\nMinimum Balance Inquiry: %s\n"
                  "Current Balance:" %
                  (self.address, self.machine_status, self.last_refill_date,
                   self.next_refill_date, self.current_balance))
        return string