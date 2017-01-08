from django.contrib import admin
from .models import Account, Operation


class OperationAdmin(admin.ModelAdmin):
    readonly_fields = ['gross_amount', 'vat_amount', 'input_date', 'id', ]

admin.site.register(Account)
admin.site.register(Operation, OperationAdmin)
