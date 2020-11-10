from django.contrib import admin
from .models import Card, User

# Register your models here.
admin.site.register(Card)
admin.site.register(User)


class CardAdmin(admin.ModelAdmin):
    readonly_fields = ['date_of_issue']


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['account_number', 'balance']