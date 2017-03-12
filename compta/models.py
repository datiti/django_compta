from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from uuid import uuid4
from compta.datiti.compta import OperationUtils


class Account(models.Model):
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    id = models.CharField(verbose_name=_('Identifier'), primary_key=True, editable=True, max_length=25)
    label = models.CharField(verbose_name=_('Label'), blank=False, editable=True, max_length=255)
    description = models.CharField(verbose_name=_('Description'), blank=True, editable=True, max_length=1024)

    def __str__(self):
        return self.label


class OperationManager(models.Manager):
    def operation_count(self, account):
        return self.filter(account=account).count()


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
    vat_rate = models.DecimalField(verbose_name=_('VAT rate'), decimal_places=2, max_digits=12, default=0,
                                   blank=True)
    apply_provision = models.BooleanField(verbose_name=_('Do apply provision?'), blank=False, default=True)
    provision_rate = models.DecimalField(verbose_name=_('Provision rate'), decimal_places=2, max_digits=12, default=40,
                                         blank=True)
    comment = models.CharField(verbose_name=_('Comment'), blank=True, max_length=1024)

    utils = None

    objects = OperationManager()

    def init_utils(self):
        if self.utils is None:
            self.utils = OperationUtils(amount=self.amount,
                                        vat_rate=self.vat_rate,
                                        apply_vat=self.apply_vat,
                                        all_tax_included=self.all_tax_included,
                                        apply_provision=self.apply_provision,
                                        provision_rate=self.provision_rate,
                                        debit_or_credit=self.debit_or_credit,
                                        )

    @property
    def gross_amount(self) -> float:
        self.init_utils()
        return self.utils.gross_amount()
    gross_amount.fget.short_description = _('Gross Amount (€)')

    @property
    def vat_amount(self) -> float:
        self.init_utils()
        return self.utils.vat_amount()
    vat_amount.fget.short_description = _('VAT Amount (€)')

    @property
    def provision_amount(self) -> float:
        self.init_utils()
        return self.utils.provision_amount()
    provision_amount.fget.short_description = _('Provision Amount (€)')

    def clean(self):
        validation_errors = []
        if not self.apply_vat:
            self.vat_rate = 0
        if not self.apply_provision:
            self.provision_rate = 0
        if self.amount <= 0:
            validation_errors.append(_('Amount must be a positive number'))
        if len(validation_errors) > 0:
            raise ValidationError(validation_errors)

    def __str__(self):
        return '[%s:%s][%s:%s]%s: %s €' \
               % (_('Operation Date'), self.operation_date.strftime('%Y %b %d'),
                  _('Account'), self.account, self.label, self.gross_amount)
