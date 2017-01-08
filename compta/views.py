from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import Operation
from .tables import OperationTable


def index_operations(request):
    queryset = Operation.objects.all()
    table = OperationTable(queryset)
    RequestConfig(request).configure(table)
    return render(request, 'operations/index.html', {'table': table})


