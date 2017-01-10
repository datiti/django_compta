import django_tables2 as tables
from django.utils.translation import ugettext_lazy as _
from .models import Operation


def sum_amount(table) -> float:
    total = sum(x.gross_amount for x in table.data)
    return round(total, 2)


class OperationTable(tables.Table):
    account = tables.Column(footer=_('Total Amount (€): '))
    amount = tables.Column(footer=sum_amount)
    # cannot sort on property columns
    vat_amount = tables.Column(orderable=False)
    provision_amount = tables.Column(orderable=False)

    class Meta:
        model = Operation
        # add those classes to enable bootstrap/semantic styles
        attrs = {'class': 'ui table table-bordered table-striped table-hover selectable sorting small'}
        exclude = ['id', 'input_date', ]
        fields = [
            'operation_date',
            'label',
            'debit_or_credit',
            'account',
            'amount',
            'vat_rate',
            'vat_amount',
            'provision_rate',
            'provision_amount',
            'all_tax_included',
            'apply_vat',
            'apply_provision',
        ]
