from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from uuid import uuid4


class Account(models.Model):
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    id = models.CharField(verbose_name=_('Identifier'), primary_key=True, editable=True, max_length=25)
    label = models.CharField(verbose_name=_('Label'), blank=False, editable=True, max_length=255)
    description = models.CharField(verbose_name=_('Description'), blank=True, editable=True, max_length=1024)

    def __str__(self):
        return self.label


class Operation(models.Model):
    class Meta:
        verbose_name = _('Operation')
        verbose_name_plural = _('Operations')

    DEBIT = -1
    CREDIT = 1
    DEBIT_OR_CREDIT = (
        (DEBIT, _('Debit')),
        (CREDIT, _('Credit')),
    )
    id = models.UUIDField(verbose_name=_('Identifier'), primary_key=True, editable=False, default=uuid4)
    operation_date = models.DateField(verbose_name=_('Operation Date'), blank=False, editable=True)
    input_date = models.DateField(verbose_name=_('Input Date'), blank=False, auto_now_add=True, editable=True)
    label = models.CharField(verbose_name=_('Label'), blank=False, editable=True, max_length=128)
    debit_or_credit = models.IntegerField(verbose_name=_('Debit or credit'), blank=False, choices=DEBIT_OR_CREDIT)
    account = models.ForeignKey('Account', verbose_name=_('Account'), related_name='+')
    amount = models.DecimalField(verbose_name=_('Amount'), decimal_places=2, max_digits=12, default=0)
    all_tax_included = models.BooleanField(verbose_name=_('All tax included'), default=True, blank=False)
    apply_vat = models.BooleanField(verbose_name=_('Do apply VAT?'), blank=False, default=True)
    vat_to_apply = models.DecimalField(verbose_name=_('VAT rate'), decimal_places=2, max_digits=12, default=0,
                                       blank=True)
    apply_provision = models.BooleanField(verbose_name=_('Do apply provision?'), blank=False, default=True)
    provision_rate = models.DecimalField(verbose_name=_('Provision rate'), decimal_places=2, max_digits=12, default=40,
                                         blank=True)
    comment = models.CharField(verbose_name=_('Comment'), blank=True, max_length=1024)

    @property
    def gross_amount(self) -> float:
        g = 0;
        if self.debit_or_credit and self.amount:
            g = int(self.debit_or_credit) * float(self.amount)
        return round(g, 2)
    gross_amount.fget.short_description = _('Gross Amount (€)')

    @property
    def vat_amount(self):
        vat_amount = 0;
        if self.apply_vat and self.vat_to_apply > 0 and self.amount:
            if self.all_tax_included:
                vat_amount = self.amount - self.amount / (1 + self.vat_to_apply/100)
            else:
                vat_amount = self.amount * self.vat_to_apply/100
        return round(vat_amount, 2)
    vat_amount.fget.short_description = _('VAT Amount (€)')

    def clean(self):
        validation_errors = []
        if self.amount <= 0:
            validation_errors.append(_('Amount must be a positive number'))
        if len(validation_errors) > 0:
            raise ValidationError(validation_errors)

    def __str__(self):
        return '[%s:%s][%s:%s]%s: %s €' \
               % (_('Operation Date'), self.operation_date.strftime('%Y %b %d'),
                  _('Account'), self.account, self.label, self.gross_amount)