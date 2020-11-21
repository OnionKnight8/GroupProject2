from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import Card, Customer, ATMMachine, Transaction


# Register your models here.
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner_id', 'card_status')
    readonly_fields = ['id', 'date_of_issue']
    list_filter = ('card_status', 'date_of_issue', 'expiry_date')

    fieldsets = (
        (None, {
            'fields': ('id', 'owner_id', 'date_of_issue')
        }),
        ('Edit:', {
            'fields': ('card_status', 'expiry_date')
        }),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'address')
    readonly_fields = ['id', 'balance']
    list_filter = ('user', 'id')

    fieldsets = (
        (None, {
            'fields': ('id', 'user', 'balance')
        }),
        ('Edit:', {
            'fields': ('pin_number', 'address', 'phone_number')
        })
    )


@admin.register(ATMMachine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'machine_status', 'last_refill_date', 'next_refill_date', 'current_balance')
    readonly_fields = ['id', 'current_balance', 'last_refill_date']
    list_filter = ['machine_status']

    fieldsets = (
        (None, {
            'fields': ('id', 'address')
        }),
        ('Refill Status:', {
            'fields': ('last_refill_date', 'next_refill_date', 'current_balance')
        }),
        ('Edit:', {
            'fields': ('machine_status', 'min_balance_inquiry')
        })
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'transaction_type', 'transaction_status', 'card_id')
    readonly_fields = ['id', 'date']
    list_filter = ('date', 'transaction_status', 'transaction_type')

    fieldsets = (
        (None, {
            'fields': ('id', 'date', 'machine_id')
        }),
        ('User Info:', {
            'fields': ('card_id', 'transfer_id')
        }),
        ('Transaction Info:', {
            'fields': ('transaction_type', 'transaction_status', 'response_code')
        })
    )