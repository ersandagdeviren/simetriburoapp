from django.contrib import admin
from .models import unit, product ,brand, currency,mainCategory,category,location,customer,currencyRate, taxoffice
# Register your models here.
admin.site.register(unit)
admin.site.register(product)
admin.site.register(currency)
admin.site.register(brand)
admin.site.register(mainCategory)
admin.site.register(category)
admin.site.register(location)
admin.site.register(customer)
admin.site.register(currencyRate)
admin.site.register(taxoffice)


