from django.contrib import admin
from .models import unit, Product, brand, currency, mainCategory, category, location, Customer, currencyRate, taxoffice, Order, OrderItem, Invoice, CashRegister, ExpenseItem, PaymentReceipt, BuyingInvoice,CustomerUpdateRequest, Place,Inventory,Transfer,Production,Supplier,BuyingItem

admin.site.register(unit)
admin.site.register(currency)
admin.site.register(brand)
admin.site.register(mainCategory)
admin.site.register(category)
admin.site.register(location)

admin.site.register(currencyRate)
admin.site.register(taxoffice)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Invoice)
admin.site.register(CashRegister)
admin.site.register(ExpenseItem)
admin.site.register(BuyingInvoice)
admin.site.register(CustomerUpdateRequest)
admin.site.register(Place)
admin.site.register(Inventory)
admin.site.register(Transfer)
admin.site.register(Production)
admin.site.register(Supplier)
admin.site.register(BuyingItem)

@admin.register(PaymentReceipt)
class PaymentReceiptAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'amount', 'usd_amount', 'eur_amount', 'date', 'transaction_number')
    fields = ('user', 'cash_register', 'customer', 'supplier', 'expense_item', 'transaction_type', 'amount', 'usd_amount', 'eur_amount', 'date', 'transaction_number')



class ProductAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('codeUyum', 'code', 'description', 'unit', 'status', 'brand', 'priceSelling', 'tax', 'currency', 'final_product')
    
    # Fields to search
    search_fields = ('codeUyum', 'description', 'barcode', 'code')
    
    # Filters
    list_filter = ('status', 'brand', 'mainCategory', 'category', 'final_product', 'currency')
    
    # Optional: Define how many records to show per page
    list_per_page = 25

# Register the Product model with the custom ProductAdmin class
admin.site.register(Product, ProductAdmin)

class CustomerAdmin(admin.ModelAdmin):
    # List display
    list_display = ('customerCode', 'companyName', 'taxOffice', 'tax_number', 'city', 'email', 'telephone', 'customerType')
    
    # Searchable fields
    search_fields = ('customerCode', 'companyName', 'taxOffice', 'tax_number', 'email', 'telephone', 'contactPerson')
    
    # List filters
    list_filter = ('city', 'district', 'country', 'customerType', 'E_invoice')
admin.site.register(Customer,CustomerAdmin)