# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-08 21:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compta', '0002_operation_all_tax_included'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operation',
            old_name='vat_to_apply',
            new_name='vat_rate',
        ),
    ]
