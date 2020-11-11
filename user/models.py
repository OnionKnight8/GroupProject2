from django.db import models
from django.contrib.auth.models import User
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
