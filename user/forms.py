from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Card, Customer, Transaction
from datetime import datetime, timedelta


class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('pin_number', 'address', 'phone_number')


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('transaction_type', 'card_id', 'machine_id', 'transaction_amount')

    # Custom init so that only DEPOSIT and WITHDRAWAL options are available here.
    def __init__(self, *args, **kwargs):
        DEPOSIT = 'DE'
        WITHDRAWAL = 'WI'
        TRANSACTION_TYPE_CHOICES = (
            (DEPOSIT, 'Deposit'),
            (WITHDRAWAL, 'Withdrawal'),
        )
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['transaction_type'] = forms.ChoiceField(
            choices=TRANSACTION_TYPE_CHOICES)


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('transaction_amount', 'transfer_id')