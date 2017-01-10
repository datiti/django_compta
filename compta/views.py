from django_tables2 import RequestConfig
from .models import Operation
from .tables import OperationTable
from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
import django_excel as excel
from django.utils.translation import ugettext as _
import xlwt
from openpyxl import Workbook


def index_operations(request):
    queryset = Operation.objects.all()
    table = OperationTable(queryset)
    RequestConfig(request).configure(table)
    return render(request, 'operations/index.html', {'table': table})


def export_data_openpyxl(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="operations.xls"'

    wb = Workbook()
    ws = wb.active
    ws.title='Operations'

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        _('operation_date'),
        _('label'),
        _('debit_or_credit'),
        _('account'),
        _('amount'),
        _('vat_rate'),
        _('vat_amount'),
        _('provision_rate'),
        _('provision_amount'),
        _('all_tax_included'),
        _('apply_vat'),
        _('apply_provision'),
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Operation.objects.all().values_list('operation_date',
                                               'label',
                                               'debit_or_credit',
                                               'account',
                                               'amount',
                                               'vat_rate',
                                               'provision_rate',
                                               'all_tax_included',
                                               'apply_vat',
                                               'apply_provision')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_data_xlwt(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="operations.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Operations')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        _('operation_date'),
        _('label'),
        _('debit_or_credit'),
        _('account'),
        _('amount'),
        _('vat_rate'),
        _('vat_amount'),
        _('provision_rate'),
        _('provision_amount'),
        _('all_tax_included'),
        _('apply_vat'),
        _('apply_provision'),
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Operation.objects.all().values_list('operation_date',
                                               'label',
                                               'debit_or_credit',
                                               'account',
                                               'amount',
                                               'vat_rate',
                                               'provision_rate',
                                               'all_tax_included',
                                               'apply_vat',
                                               'apply_provision')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_operations(request, atype):
    if atype == 'data':
        data = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        sheet = excel.pe.Sheet(data)
        return excel.make_response(sheet, 'xlsx')
    elif atype == "sheet2":
        return excel.make_response_from_a_table(
            Operation,
            'xlsx',
            file_name='sheet2')
    elif atype == "sheet":
        query_sets = Operation.objects.all().values_list('operation_date',
                                                         'label',
                                                         'debit_or_credit',
                                                         'account',
                                                         'amount',
                                                         'vat_rate',
                                                         'provision_rate',
                                                         'all_tax_included',
                                                         'apply_vat',
                                                         'apply_provision')
        column_names = [
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
        return excel.make_response_from_array(
            query_sets,
            'xlsx',
            file_name='sheet'
        )
#        return excel.make_response_from_a_table(
#            Operation, 'xlsx', file_name="sheet")
    else:
        return HttpResponseBadRequest(
            "Bad request. please put one of these " +
            "in your url suffix: sheet, book or custom")


