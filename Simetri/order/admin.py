from django.contrib import admin
from .models import unit, Product, brand, currency, mainCategory, category, location, Customer, currencyRate, taxoffice, Order, OrderItem, Invoice, CashRegister, ExpenseItem, PaymentReceipt, BuyingInvoice,CustomerUpdateRequest

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
admin.site.register(Invoice)
admin.site.register(CashRegister)
admin.site.register(ExpenseItem)
admin.site.register(BuyingInvoice)
admin.site.register(CustomerUpdateRequest)


class PaymentReceiptAdmin(admin.ModelAdmin):
    list_display = ('user', 'cash_register', 'customer', 'transaction_type', 'amount', 'usd_amount', 'eur_amount', 'date', 'transaction_number')
    readonly_fields = ('usd_amount', 'eur_amount', 'transaction_number')

admin.site.register(PaymentReceipt, PaymentReceiptAdmin)
