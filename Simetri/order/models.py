from django.db import models
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import urllib.request
from django.utils import timezone



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
    country = models.CharField(max_length=50, blank=True, default="Türkiye")
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=11, blank=True)
    customerType = models.CharField(max_length=50, blank=True)
    contactPerson = models.CharField(max_length=50, blank=True)
   
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
            self.order_number = f"{date_prefix}{new_order_number:05d}"
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_orders")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)

    def __str__(self):
        return f"{self.order.order_number} - {self.product.description}"