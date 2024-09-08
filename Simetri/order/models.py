from django.db import models
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import requests
from bs4 import BeautifulSoup
import re
import urllib.request
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
User = get_user_model()

def get_currency_rates():
    try:
        webpage_response = requests.get('https://canlidoviz.com/doviz-kurlari/garanti-bankasi')
        webpage = webpage_response.content
        soup = BeautifulSoup(webpage, "html.parser")
        target_data_usd = soup.select_one(
            "body > div.flex.w-full.justify-center.px-3 > div > div.flex.flex-col.sc1300\:flex-row.justify-center.max-w-\[1500px\].gap-3.min-w-0 > div > div.flex.gap-3.w-full.flex-col.lg\:flex-row > div.w-full > div.flex.lg\:px-3.flex-col.flex-\[1_1_auto\].lg\:bg-pholder.lg\:theme-dark\:bg-dPholder.lg\:theme-light\:bg-wPholder.shadow-boxShadow > div.py-0 > table > tbody > tr:nth-child(1) > td.align-middle.md\:align-top.text-right.w-24.truncate.ml-6 > div").get_text()
        target_data_usd = round(float(str(target_data_usd).replace(" ", "").replace("\n", "")[:5]), 2)
        target_data_usd = round(target_data_usd, 2)  # Keep it as a float for now

        target_data_eur = soup.select_one(
            "body > div.flex.w-full.justify-center.px-3 > div > div.flex.flex-col.sc1300\:flex-row.justify-center.max-w-\[1500px\].gap-3.min-w-0 > div > div.flex.gap-3.w-full.flex-col.lg\:flex-row > div.w-full > div.flex.lg\:px-3.flex-col.flex-\[1_1_auto\].lg\:bg-pholder.lg\:theme-dark\:bg-dPholder.lg\:theme-light\:bg-wPholder.shadow-boxShadow > div.py-0 > table > tbody > tr:nth-child(2) > td.align-middle.md\:align-top.text-right.w-24.truncate.ml-6 > div").get_text()
        target_data_eur = round(float(str(target_data_eur).replace(" ", "").replace("\n", "")[:5]), 2)
        target_data_eur = round(target_data_eur, 2)  # Keep it as a float for now
    except:
        target_data_usd=0
        target_data_eur=0

        
    try:
        webpage_response2 = requests.get('https://www.altinkaynak.com/Doviz/Kur/Guncel')
        webpage2 = webpage_response2.content
        soup2 = BeautifulSoup(webpage2, "html.parser")
        target_data_usd2 = round(float(soup2.find(id="tdUSDSell").get_text().replace(",", ".")), 2)
        target_data_usd2 = round(target_data_usd2, 2)  # Keep it as a float for now

        target_data_eur2 = round(float(soup2.find(id="tdEURSell").get_text().replace(",", ".")), 2)
        target_data_eur2 = round(target_data_eur2, 2)  # Keep it as a float for now
    except:
        target_data_usd2=0
        target_data_eur2=0
    return target_data_usd, target_data_eur

# Create your models here.
class location (models.Model):
    country=models.CharField(max_length=15)
    city=models.CharField(max_length=15)
    district=models.CharField(max_length=50,blank=True)


    def __str__(self):
        return self.city

class taxoffice(models.Model):
    city=models.CharField(max_length=15)
    vd=models.CharField(max_length=40)

    def __str__(self):
        return self.vd
    
class currency (models.Model):
    currency=models.CharField(max_length=3)
    def __str__(self):
        return self.currency

class currencyRate (models.Model):
    currencyUSD=models.CharField( default="USD",max_length=3)
    rateUSD=models.DecimalField(max_digits=10,decimal_places=2,blank=True)
    currencyEUR=models.CharField( default="EUR",max_length=3)
    rateEUR=models.DecimalField(max_digits=10,decimal_places=2,blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    def formatted_date(self):
        return self.date.strftime('%d-%m-%Y')
    def __str__(self):
        return f"Currency rates for {self.formatted_date()}"

class brand (models.Model):
    brand=models.CharField(max_length=10)
    def __str__(self):
        return self.brand
class unit (models.Model):
    unitProduct=models.CharField(max_length=5)
    def __str__(self):
        return self.unitProduct
 
class mainCategory (models.Model):
    mainCategory=models.CharField(max_length=15)
    def __str__(self):
        return self.mainCategory

class category (models.Model):
    category=models.CharField(max_length=20)
    category_tr=models.CharField(max_length=20 ,null=True, blank=True)
    final_product=models.BooleanField(default=True,null=True, blank=True)

    def __str__(self):
        return self.category

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_customers",blank=True,null=True)
    customerCode = models.CharField(max_length=50)
    companyName = models.CharField(max_length=150)
    taxOffice = models.CharField(max_length=50)
    tax_number = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=100, blank=True)
    middleName = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    adress = models.TextField(blank=True)
    shipping_adress=models.CharField(max_length=300, blank=True)
    country = models.CharField(max_length=50, blank=True, default="Türkiye")
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    customerType = models.CharField(max_length=50, blank=True)
    contactPerson = models.CharField(max_length=50, blank=True)
    E_invoice=models.BooleanField(default=True)
   
    def __str__(self):
        return self.companyName
class Supplier(models.Model):
    supplierCode = models.CharField(max_length=50)
    companyName = models.CharField(max_length=50)
    taxOffice = models.CharField(max_length=50, null=True, blank=True)
    tax_number = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    adress = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=50, blank=True)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=11, null=True, blank=True)
    contactPerson = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.companyName
    
class Place(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    codeUyum = models.CharField(max_length=50)
    code = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=300)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, related_name="unit_name")
    status = models.BooleanField(default=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name="brand_name")
    barcode = models.CharField(max_length=50, blank=True)
    mainCategory = models.ForeignKey('MainCategory', on_delete=models.CASCADE, related_name="mainCategories_name")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="categories_name")
    priceSelling = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    priceSelling2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    priceSelling3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    tax = models.PositiveIntegerField(blank=True, default=20)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name="currency_name")
    photoPath = models.CharField(max_length=1000, blank=True)
    final_product=models.BooleanField(default=True)

    def __str__(self):
        return self.codeUyum

class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="customer_orders")
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_orders")
    is_billed = models.BooleanField(default=False)

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            current_date = timezone.now()
            date_prefix = current_date.strftime('%Y%m')
            last_order = Order.objects.filter(order_number__startswith=date_prefix).order_by('order_number').last()
            if last_order:
                last_order_number = int(last_order.order_number[-5:])
                new_order_number = last_order_number + 1
            else:
                new_order_number = 1
            self.order_number = f"{date_prefix}{new_order_number:08d}"
        super().save(*args, **kwargs)

        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_orders")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    currency_rate=models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    discount_rate=models.PositiveIntegerField(blank=True, default=0)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=20)  # Add this line
    def __str__(self):
        return f"{self.order.order_number} - {self.product.description}"

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="invoice")
    invoice_date = models.DateTimeField(auto_now_add=True)
    billing_address = models.CharField(max_length=250, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    grand_total_USD = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    grand_total_EUR = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    status = models.CharField(max_length=50, default='Pending')
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.invoice_number

    def save(self, *args, **kwargs):
        is_new = self.pk is None 
        if not self.invoice_number:
            current_date = timezone.now()
            customer = self.order.customer
            date_prefix = current_date.strftime('%Y%m')

            if not customer.E_invoice:
                prefix = "SMR"
            else:
                prefix = "SMT"

            if not customer.tax_number:
                filter_prefix = date_prefix
                last_invoice = Invoice.objects.filter(invoice_number__startswith=filter_prefix).order_by('invoice_number').last()
                if last_invoice:
                    last_invoice_number = int(last_invoice.invoice_number[-5:])
                    new_invoice_number = last_invoice_number + 1
                else:
                    new_invoice_number = 1
                self.invoice_number = f"{filter_prefix}{new_invoice_number:05d}"
            else:
                filter_prefix = f"{prefix}{date_prefix}"
                last_invoice = Invoice.objects.filter(invoice_number__startswith=filter_prefix).order_by('invoice_number').last()
                if last_invoice:
                    last_invoice_number = int(last_invoice.invoice_number[-5:])
                    new_invoice_number = last_invoice_number + 1
                else:
                    new_invoice_number = 1
                self.invoice_number = f"{filter_prefix}{new_invoice_number:05d}"
        
        # Check stock amounts before saving
        for item in self.order.order_items.all():
            product = item.product
            inventory = product.inventory_set.filter(place__name="D1").first()  # Adjust place name as needed
            if inventory is None or inventory.quantity < item.quantity:
                if not is_new:
                    pass
                else:
                    raise ValueError(f"Not enough stock for product {product.description} in D1.")

        super().save(*args, **kwargs)

        # Adjust stock amounts after saving
        for item in self.order.order_items.all():
            product = item.product
            inventory = product.inventory_set.filter(place__name="D1").first()  # Adjust place name as needed
            if is_new:
                inventory.quantity -= item.quantity
                inventory.save()
            else:
                product.save()

        # Mark the associated order as billed
        self.order.is_billed = True
        self.order.save()

    def delete(self, *args, **kwargs):
        # Increase the stock amounts before deleting the invoice
        for item in self.order.order_items.all():
            product = item.product
            inventory = product.inventory_set.filter(place__name="D1").first()  # Adjust place name as needed
            if inventory:
                inventory.quantity += item.quantity
                inventory.save()

        # Mark the associated order as unbilled before deleting the invoice
        self.order.is_billed = False
        self.order.save()
        super().delete(*args, **kwargs)


class CashRegister(models.Model):
    cash_code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    currency = models.ForeignKey(currency, on_delete=models.CASCADE, related_name="currency_name_bank")
    balance_USD = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_EUR = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_tl = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return self.name

    def transfer(self, amount, target_register, fee, expense_item, user):
        # Assume the amount is in balance_tl for simplicity. You can extend this to other currencies.
        if self.balance_tl >= amount + fee:
            self.balance_tl -= amount
            target_register.balance_tl += amount
            self.save()
            target_register.save()
        if self.balance_USD >= amount + fee:
            self.balance_USD -= amount
            target_register.balance_USD += amount
            self.save()
            target_register.save()
        if self.balance_EUR >= amount + fee:
            self.balance_EUR -= amount
            target_register.balance_EUR += amount
            self.save()
            target_register.save()
            
            # Create a transaction record for the source register
            Transaction.objects.create(
                user=user,
                cash_register=self,
                target_register=target_register,
                transaction_type=Transaction.TRANSFER_OUT,
                amount=amount,
                fee=fee,
                expense_item=expense_item
            )
            
            # Create a transaction record for the target register
            Transaction.objects.create(
                user=user,
                cash_register=target_register,
                transaction_type=Transaction.TRANSFER_IN,
                amount=amount,
                fee=fee
            )
            
            # Record the transfer fee as an expense
            PaymentReceipt.objects.create(
                user=user,
                cash_register=self,
                expense_item=expense_item,
                transaction_type=PaymentReceipt.PAYMENT,
                amount=fee
            )
            return True
        return False
    
class ExpenseItem(models.Model):
    expense_code=models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PaymentReceipt(models.Model):
    RECEIPT = 'Tahsilat'
    PAYMENT = 'Tediye'
    TRANSACTION_TYPES = [
        (RECEIPT, 'Tahsilat'),
        (PAYMENT, 'Tediye'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cash_register = models.ForeignKey(CashRegister, on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT, null=True, blank=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.PROTECT, null=True, blank=True)
    expense_item = models.ForeignKey(ExpenseItem, on_delete=models.CASCADE, null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    usd_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=True, null=True, blank=True)
    eur_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=True, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    transaction_number = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        usd_rate, eur_rate = get_currency_rates()
        
        usd_rate = Decimal(usd_rate)
        eur_rate = Decimal(eur_rate)

        if self.amount is not None:
            self.amount = Decimal(self.amount)
            self.usd_amount = self.amount / usd_rate
            self.eur_amount = self.amount / eur_rate
        
        elif self.usd_amount is not None:
            self.usd_amount = Decimal(self.usd_amount)
            self.amount = self.usd_amount * usd_rate
            self.eur_amount = self.usd_amount * usd_rate / eur_rate
          
        elif self.eur_amount is not None:
            self.eur_amount = Decimal(self.eur_amount)
            self.amount = self.eur_amount * eur_rate
            self.usd_amount = self.eur_amount * eur_rate / usd_rate
           
        if not self.transaction_number:
            current_date = timezone.now()
            date_prefix = current_date.strftime('%Y%m%d')

            if self.transaction_type == self.RECEIPT and self.customer and self.customer.tax_number:
                prefix = "THS"
            elif self.transaction_type == self.PAYMENT:
                prefix = "ODM"
            else:
                prefix = ""

            if prefix:
                filter_prefix = f"{prefix}{date_prefix}"
                last_transaction = PaymentReceipt.objects.filter(transaction_number__startswith=filter_prefix).order_by('transaction_number').last()
                if last_transaction:
                    last_transaction_number = int(last_transaction.transaction_number[-5:])
                    new_transaction_number = last_transaction_number + 1
                else:
                    new_transaction_number = 1
                self.transaction_number = f"{filter_prefix}{new_transaction_number:05d}"

        if self.transaction_type == self.RECEIPT:
            if self.amount is not None:
                self.cash_register.balance_tl += self.amount
            if self.usd_amount is not None:
                self.cash_register.balance_USD += self.usd_amount
            if self.eur_amount is not None:
                self.cash_register.balance_EUR += self.eur_amount
        elif self.transaction_type == self.PAYMENT:
            if self.amount is not None:
                self.cash_register.balance_tl -= self.amount
            if self.usd_amount is not None:
                self.cash_register.balance_USD -= self.usd_amount
            if self.eur_amount is not None:
                self.cash_register.balance_EUR -= self.eur_amount
        self.cash_register.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.transaction_type == self.RECEIPT:
            if self.amount is not None:
                self.cash_register.balance_tl -= self.amount
            if self.usd_amount is not None:
                self.cash_register.balance_USD -= self.usd_amount
            if self.eur_amount is not None:
                self.cash_register.balance_EUR -= self.eur_amount
        elif self.transaction_type == self.PAYMENT:
            if self.amount is not None:
                self.cash_register.balance_tl += self.amount
            if self.usd_amount is not None:
                self.cash_register.balance_USD += self.usd_amount
            if self.eur_amount is not None:
                self.cash_register.balance_EUR += self.eur_amount

        self.cash_register.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.transaction_type} - {self.amount}"
    

class Transaction(models.Model):
    TRANSFER_OUT = 'Out'
    TRANSFER_IN = 'In'
    TRANSACTION_TYPES = [
        (TRANSFER_OUT, 'Out'),
        (TRANSFER_IN, 'In'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cash_register = models.ForeignKey(CashRegister, on_delete=models.CASCADE, related_name='transactions')
    target_register = models.ForeignKey(CashRegister, on_delete=models.CASCADE, related_name='incoming_transactions', null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expense_item = models.ForeignKey(ExpenseItem, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.transaction_type} - {self.amount}"
    
class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    priceBuying = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True, default=0)

    class Meta:
        unique_together = ('product', 'place')

    def update_quantity(self, quantity, increase=True):
        if increase:
            self.quantity += quantity
        else:
            self.quantity -= quantity
        self.save()

    def __str__(self):
        return f"{self.product} at {self.place}"

class BuyingInvoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT,null=True, blank=True, related_name="supplier_invoices")
    invoice_date = models.DateTimeField(auto_now_add=True)
    billing_address = models.CharField(max_length=250, blank=True, null=True)
    total_amount_tl = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    total_amount_USD = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    total_amount_EUR = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    grand_total_tl = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    grand_total_USD = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    grand_total_EUR = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return self.invoice_number

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            current_date = timezone.now()
            date_prefix = current_date.strftime('%Y%m')
            prefix = "BYI"
            filter_prefix = f"{prefix}{date_prefix}"
            last_invoice = BuyingInvoice.objects.filter(invoice_number__startswith=filter_prefix).order_by('invoice_number').last()
            if last_invoice:
                last_invoice_number = int(last_invoice.invoice_number[-5:])
                new_invoice_number = last_invoice_number + 1
            else:
                new_invoice_number = 1
            self.invoice_number = f"{filter_prefix}{new_invoice_number:05d}"

        super().save(*args, **kwargs)

    def update_totals(self):
        self.total_amount_tl = 0
        self.total_amount_USD = 0
        self.total_amount_EUR = 0
        self.total_discount = 0
        self.tax_amount = 0
        self.grand_total_tl = 0

        for item in self.buying_items.all():
            currency_rate = item.currency_rate
            discount_amount = item.price * item.discount_rate / 100
            tl_value = round((item.price - discount_amount) * currency_rate * item.quantity, 2)
            item_tax = round(tl_value * item.tax / 100, 2)
            item_total = tl_value + item_tax
            self.total_amount_tl += tl_value
            self.tax_amount += item_tax
            self.total_discount += round(discount_amount * item.quantity * currency_rate, 2)

            if str(item.product.currency) == "USD":
                self.total_amount_USD += item.price * item.quantity
            if str(item.product.currency) == "EUR":
                self.total_amount_EUR += item.price * item.quantity

        self.grand_total_tl = self.total_amount_tl + self.tax_amount
        self.grand_total_USD = self.total_amount_USD
        self.grand_total_EUR = self.total_amount_EUR
        self.save()

class BuyingItem(models.Model):
    buying_invoice = models.ForeignKey(BuyingInvoice, on_delete=models.CASCADE, related_name="buying_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    currency_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    discount_rate = models.PositiveIntegerField(blank=True, default=0)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=20)  # Add this line

    def __str__(self):
        return f"{self.buying_invoice.invoice_number} - {self.product.description}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.buying_invoice.update_totals()

    def delete(self, *args, **kwargs):
        invoice = self.buying_invoice
        self.inventory.update_quantity(self.quantity, increase=False)  # Decrease the inventory
        super().delete(*args, **kwargs)
        invoice.update_totals()



class CustomerUpdateRequest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='update_requests')
    updated_data = models.JSONField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Update Request for {self.customer}'

class Transfer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    from_place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='transfers_from')
    to_place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='transfers_to')
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from_inventory, created = Inventory.objects.get_or_create(product=self.product, place=self.from_place)
        to_inventory, created = Inventory.objects.get_or_create(product=self.product, place=self.to_place)
        
        # Update inventory quantities
        from_inventory.quantity -= self.quantity
        from_inventory.save()
        
        to_inventory.quantity += self.quantity
        to_inventory.save()

    def __str__(self):
        return f"Transfer {self.quantity} of {self.product} from {self.from_place} to {self.to_place} on {self.date}"

class Production(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productions")
    chip = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="chip_productions")
    empty_cartridge = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="empty_cartridge_productions")
    cartridge_head = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="cartridge_head_productions")
    box = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="box_productions")
    waste_box = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="waste_box_productions")
    powder = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="powder_productions")
    powder_gram = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    developer = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="developer_productions")
    developer_gram = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Production of {self.product}"


