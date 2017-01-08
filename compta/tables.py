import django_tables2 as tables
from .models import Operation


class OperationTable(tables.Table):
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
