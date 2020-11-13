from django.contrib import admin
from .models import Card, Customer


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
    readonly_fields = ['user', 'id']
    list_filter = ('user', 'id')

    fieldsets = (
        (None, {
            'fields': ('id', 'user')
        }),
        ('Edit:', {
            'fields': ('pin_number', 'address', 'phone_number')
        })
    )
