from django.db import models


class ContractManagers(models.Manager):
    def get_subject_contract_name(self):
        return self.order_by('customer', 'subject_contract')
