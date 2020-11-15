from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator
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

    balance = models.DecimalField(default=0, help_text="User's balance.", blank=False,
                                  decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0'))],)

    # Regex validator used to verify phone number
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: "
                                         "'+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False,
                                    help_text="The user's phone number.")

    # Methods:
    def __str__(self):
        string = ("Username: %s\n" %
                  (self.user,))
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
    current_balance = models.DecimalField(default=0, decimal_places=2, max_digits=12,
                                          validators=[MinValueValidator(Decimal('0'))],
                                          help_text="Machine's current balance.", blank=False, )

    # Methods
    def __str__(self):
        string = ("Address: %s\n" %
                  (self.address,))
        return string


class Transaction(models.Model):
    # Fields:
    date = models.DateTimeField(auto_now=True, help_text= "The date and time the transaction was performed.", )
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE, help_text="Card from which transaction was performed.",)
    machine_id = models.ForeignKey(ATMMachine, on_delete=models.CASCADE,
                                   help_text="ATM from which transaction was performed.")

    # Transaction Status Options
    COMPLETED = 'CO'
    CANCELED = 'CA'
    TRANSACTION_STATUS_CHOICES = (
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
    )
    transaction_status = models.CharField(max_length=10, choices=TRANSACTION_STATUS_CHOICES, default=COMPLETED,
                                          help_text="Status of transaction.", )

    # ATM response codes from https://www.cardaccess.com.au/bank-response-codes/, only using relevant ones.
    TRANSACTION_APPROVED = 00
    INSUFFICIENT_FUNDS = 51
    EXPIRED_CARD = 54
    RESPONSE_CODE_CHOICES = (
        (TRANSACTION_APPROVED, 00),
        (INSUFFICIENT_FUNDS, 51),
        (EXPIRED_CARD, 54),
    )
    response_code = models.IntegerField(choices=RESPONSE_CODE_CHOICES, default=TRANSACTION_APPROVED,
                                        help_text="Transaction response codes. Refer to the following link "
                                                  "for more information: "
                                                  "https://www.cardaccess.com.au/bank-response-codes/", )

    # Choices for types of transactions
    DEPOSIT = 'DE'
    WITHDRAWAL = 'WI'
    TRANSFER = 'TR'
    TRANSACTION_TYPE_CHOICES = (
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
        (TRANSFER, 'Transfer'),
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, default=DEPOSIT, blank=False,
                                        help_text="The type of transaction to be processed.", )

    transfer_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None,
                                    help_text="User in which money is transferred to. Only used in a transfer.",
                                    related_name='receiver')

    transaction_amount = models.DecimalField(default=25, blank=False, null=False, decimal_places=2,
                                             max_digits=12, validators=[MinValueValidator(Decimal('0'))],
                                             help_text="Amount of money involved in transaction.",)

    # Methods:
    def __str__(self):
        string = ("Date: %s\nCard ID:: %s\nMachine ID: %s\nTransaction Status: %s\nResponse Coder: %s\n"
                  "Transaction Type: %s\nTransfer ID: %s\nTransaction Amount: %s\n" %
                  (self.date, self.card_id, self.machine_id, self.transaction_status, self.response_code,
                   self.transaction_type, self.transfer_id, self.transaction_amount))
        return string
