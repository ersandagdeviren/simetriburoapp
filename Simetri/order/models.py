from django.db import models
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import requests
from bs4 import BeautifulSoup
import re
import urllib.request
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

def get_currency_rates():
    webpage_response = requests.get('https://canlidoviz.com/doviz-kurlari/garanti-bankasi')
    webpage = webpage_response.content
    soup = BeautifulSoup(webpage, "html.parser")
    target_data_usd = soup.select_one("html > body > div:nth-of-type(3) > div > div:nth-of-type(3) > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(4) > table > tbody > tr:nth-of-type(1) > td:nth-of-type(3) > div > span").get_text()
    target_data_usd = Decimal(str(target_data_usd).replace(" ", "").replace("\n", "")).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    target_data_eur = soup.select_one("html > body > div:nth-of-type(3) > div > div:nth-of-type(3) > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(4) > table > tbody > tr:nth-of-type(2) > td:nth-of-type(3) > div > span").get_text()
    target_data_eur = Decimal(str(target_data_eur).replace(" ", "").replace("\n", "")).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

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
    def __str__(self):
        return self.category

class Customer(models.Model):
    customerCode = models.CharField(max_length=50)
    companyName = models.CharField(max_length=50)
    taxOffice = models.CharField(max_length=50)
    tax_number = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    middleName = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    adress = models.CharField(max_length=250, blank=True)
    shipping_adress=models.CharField(max_length=250, blank=True)
    country = models.CharField(max_length=50, blank=True, default="Türkiye")
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=11, blank=True)
    customerType = models.CharField(max_length=50, blank=True)
    contactPerson = models.CharField(max_length=50, blank=True)
    E_invoice=models.BooleanField(default=True)
   
    def __str__(self):
        return self.companyName

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
    priceBuying = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    priceSelling = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    priceSelling2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    priceSelling3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    tax = models.PositiveIntegerField(blank=True, default=20)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name="currency_name")
    stockAmount = models.PositiveIntegerField(default=0)
    photoPath = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.codeUyum

class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_orders")
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
    def __str__(self):
        return f"{self.order.order_number} - {self.product.description}"
    
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="invoice")
    invoice_date = models.DateTimeField(auto_now_add=True)
    billing_address = models.CharField(max_length=250, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    total_discount=models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    grand_total_USD = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    grand_total_EUR = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return self.invoice_number

    def save(self, *args, **kwargs):
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
        super().save(*args, **kwargs)
        # Mark the associated order as billed

        self.order.is_billed = True
        self.order.save()
        # Decrease the stock amounts
        for item in self.order.order_items.all():
            product = item.product
            product.stockAmount -= item.quantity
            product.save()


    def delete(self, *args, **kwargs):
        # Increase the stock amounts before deleting the invoice
        for item in self.order.order_items.all():
            product = item.product
            product.stockAmount += item.quantity
            product.save()

        # Mark the associated order as unbilled before deleting the invoice
        self.order.is_billed = False
        self.order.save()
        super().delete(*args, **kwargs)

class CashRegister(models.Model):
    cash_code=models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    expense_item = models.ForeignKey(ExpenseItem, on_delete=models.CASCADE, null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    usd_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True)
    eur_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True)
    date = models.DateTimeField(auto_now_add=True)
    transaction_number = models.CharField(max_length=20, unique=True, blank=True)
    def save(self, *args, **kwargs):
    # Fetch currency rates
        usd_rate, eur_rate = get_currency_rates()

        # Calculate USD and EUR amounts
        self.usd_amount = (self.amount / usd_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.eur_amount = (self.amount / eur_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        if not self.transaction_number:
            current_date = timezone.now()
            date_prefix = current_date.strftime('%Y%m%d')

            if self.transaction_type == self.RECEIPT and self.customer and self.customer.tax_number:
                prefix = "THS"
            elif self.transaction_type == self.PAYMENT:
                prefix = "ODM"
            else:
                prefix = ""

            if prefix:  # Ensures that prefix is set
                filter_prefix = f"{prefix}{date_prefix}"
                last_transaction = PaymentReceipt.objects.filter(transaction_number__startswith=filter_prefix).order_by('transaction_number').last()
                if last_transaction:
                    last_transaction_number = int(last_transaction.transaction_number[-5:])
                    new_transaction_number = last_transaction_number + 1
                else:
                    new_transaction_number = 1
                self.transaction_number = f"{filter_prefix}{new_transaction_number:05d}"

        if self.transaction_type == self.RECEIPT:
            self.cash_register.balance += self.amount
            if self.customer:
                # Credit entry for the customer
                Credit.objects.create(
                    customer=self.customer,
                    amount=self.amount,
                    date=self.date
                )
        elif self.transaction_type == self.PAYMENT:
            self.cash_register.balance -= self.amount
            if self.expense_item:
                # Debit entry for the expense item
                Debit.objects.create(
                    expense_item=self.expense_item,
                    amount=self.amount,
                    date=self.date
                )
        self.cash_register.save()
        super().save(*args, **kwargs)

    

    def delete(self, *args, **kwargs):
        if self.transaction_type == self.RECEIPT:
            self.cash_register.balance -= self.amount
            if self.customer:
                # Remove the corresponding credit entry for the customer
                Credit.objects.filter(
                    customer=self.customer,
                    amount=self.amount,
                    date=self.date
                ).delete()
        elif self.transaction_type == self.PAYMENT:
            self.cash_register.balance += self.amount
            if self.expense_item:
                # Remove the corresponding debit entry for the expense item
                Debit.objects.filter(
                    expense_item=self.expense_item,
                    amount=self.amount,
                    date=self.date
                ).delete()
        self.cash_register.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.transaction_type} - {self.amount}"

class Credit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.amount}"

class Debit(models.Model):
    expense_item = models.ForeignKey(ExpenseItem, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expense_item} - {self.amount}"

class BuyingInvoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="buying_invoice")
    invoice_date = models.DateTimeField(auto_now_add=True)
    billing_address = models.CharField(max_length=250, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
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
        
        # Mark the associated order as billed
        self.order.is_billed = True
        self.order.save()

        # Increase the stock amounts for buying invoice
        for item in self.order.order_items.all():
            product = item.product
            product.stockAmount += item.quantity
            product.save()

    def delete(self, *args, **kwargs):
        # Decrease the stock amounts before deleting the buying invoice
        for item in self.order.order_items.all():
            product = item.product
            product.stockAmount -= item.quantity
            product.save()

        # Mark the associated order as unbilled before deleting the invoice
        self.order.is_billed = False
        self.order.save()
        super().delete(*args, **kwargs)