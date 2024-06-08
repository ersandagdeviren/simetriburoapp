from django.contrib import admin
from .models import unit, Product ,brand, currency,mainCategory,category,location,Customer,currencyRate, taxoffice, Order,OrderItem
# Register your models here.
admin.site.register(unit)
admin.site.register(Product)
admin.site.register(currency)
admin.site.register(brand)
admin.site.register(mainCategory)
admin.site.register(category)
admin.site.register(location)
admin.site.register(Customer)
admin.site.register(currencyRate)
admin.site.register(taxoffice)
admin.site.register(Order)
admin.site.register(OrderItem)

