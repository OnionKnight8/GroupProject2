"""
Author: Team 2
Description: Class for ATM cards.
"""


class AdminCard:

    # Initializer
    def __init__(self, date_of_issue, expiry_date, card_status):
        self.date_of_issue = date_of_issue
        self.expiry_date = expiry_date
        self.card_status = card_status

    # Get and set methods for each class variable:

    def get_date_of_issue(self):
        return self.date_of_issue

    def set_date_of_issue(self, date_of_issue):
        self.date_of_issue = date_of_issue

    def get_expiry_date(self):
        return self.expiry_date

    def set_expiry_date(self, expiry_date):
        self.expiry_date = expiry_date

    def get_card_status(self):
        return self.card_status

    def set_card_status(self, card_status):
        self.card_status = card_status

    # String representation of class:
    def __str__(self):
        string = ("Date of Issue: %s\nExpiry Date: %s\nCard Status: %s\n" %
               (self.date_of_issue, self.expiry_date, self.card_status))
        return string