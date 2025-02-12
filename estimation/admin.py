from django.contrib import admin

from .models import Act, Addendum, Company, Contract


admin.site.register(Act)
admin.site.register(Addendum)
admin.site.register(Company)
admin.site.register(Contract)
