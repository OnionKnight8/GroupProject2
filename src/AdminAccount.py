"""
Author: Team 2
Description: Class for accounts.
"""


class AdminAccount:

    def __init__(self, account_number, pin, account_name, address, balance, phone_number):
        self.account_number = account_number
        self.pin = pin
        self.account_name = account_name
        self.address = address
        self.balance = balance
        self.phone_number = phone_number

    # Get and set methods for each class variable:

    def get_account_number(self):
        return self.account_number

    def set_account_number(self, account_number):
        self.account_number = account_number

    def get_pin(self):
        return self.pin

    def set_pin(self, pin):
        self.pin = pin

    def get_account_name(self):
        return self.account_name

    def set_account_name(self, account_name):
        self.account_name = account_name

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_balance(self):
        return self.balance

    def set_balance(self, balance):
        self.balance = balance

    def get_phone_number(self):
        return self.phone_number

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number

    # String representation of class:
    def __str__(self):
        string = ("""Account Number: %s\nPIN: %s\nAccount Name: %s\n
        Address: %s\nBalance: %s\nPhone Number: %s\n""" %
                  (self.account_number, self.pin, self.account_name,
                   self.address, self.balance, self.phone_number))
        return string