from django.contrib import admin

from .models import Company, Contract, Act


admin.site.register(Company)
admin.site.register(Contract)
admin.site.register(Act)
