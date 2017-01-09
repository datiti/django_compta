
class OperationUtils:
    def __init__(self, debit_or_credit: int, apply_vat: bool, all_tax_included: bool, vat_rate: float, provision_rate: float, apply_provision: bool, amount: float):
        self.apply_vat = apply_vat
        self.all_tax_included = all_tax_included
        self.vat_rate = vat_rate
        self.amount = amount
        self.provision_rate = provision_rate
        self.apply_provision = apply_provision
        self.debit_or_credit = debit_or_credit

    def vat_amount(self) -> float:
        """
        Compute the vat amount given the amount, the rate and choice parameters
        :return: the vat amount for the given amount
        """
        vat_amount = 0
        if self.apply_vat and self.vat_rate > 0 and self.amount:
            if self.all_tax_included:
                vat_amount = self.amount - self.amount / (1 + self.vat_rate / 100)
            else:
                vat_amount = self.amount * self.vat_rate / 100
        return round(vat_amount, 2)

    def provision_amount(self) -> float:
        """
        Returns the provision amount for the given amount and provision rate
        :return: the provision amount for the given amount and provision rate
        """
        p = 0
        if self.apply_provision and self.provision_rate and self.amount:
            p = (self.amount - self.vat_amount()) * self.provision_rate/100
        return round(p, 2)

    def gross_amount(self) -> float:
        g = 0
        if self.debit_or_credit and self.amount:
            g = int(self.debit_or_credit) * float(self.amount)
        return round(g, 2)
