from django.db import models
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import urllib.request

def currency():
    
    webpage_response = requests.get('https://canlidoviz.com/doviz-kurlari/garanti-bankasi')
    webpage = webpage_response.content
    soup = BeautifulSoup(webpage, "html.parser")
    target_data_usd = soup.select_one("html > body > div:nth-of-type(3) > div > div:nth-of-type(3) > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(4) > table > tbody > tr:nth-of-type(1) > td:nth-of-type(3) > div > span").get_text()
    target_data_usd=round(float(str(target_data_usd).replace(" ","").replace("\n","")),2)
    target_data_eur=soup.select_one("html > body > div:nth-of-type(3) > div > div:nth-of-type(3) > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(4) > table > tbody > tr:nth-of-type(2) > td:nth-of-type(3) > div > span").get_text()
    target_data_eur=round(float(str(target_data_eur).replace(" ","").replace("\n","")),2)

    return(target_data_usd,target_data_eur)

defaultcurrency=currency()
defaultUSD=defaultcurrency[0]
defaultEUR=defaultcurrency[1]



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
    rateUSD=models.DecimalField(max_digits=10,decimal_places=2,blank=True,default=defaultUSD)
    currencyEUR=models.CharField( default="EUR",max_length=3)
    rateEUR=models.DecimalField(max_digits=10,decimal_places=2,blank=True,default=defaultEUR)
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
class product (models.Model):
    codeUyum=models.CharField(max_length=50)
    code= models.CharField(max_length=50,blank=True)
    description=models.CharField(max_length=300)
    unit=models.ForeignKey(unit, on_delete=models.CASCADE, related_name="unit_name")
    status=models.BooleanField(default=True)
    brand=models.ForeignKey(brand, on_delete=models.CASCADE, related_name="brand_name")
    barcode=models.CharField(max_length=50,blank=True)
    mainCategory=models.ForeignKey(mainCategory, on_delete=models.CASCADE, related_name="mainCategories_name")
    category=models.ForeignKey(category, on_delete=models.CASCADE, related_name="categories_name")
    priceBuying=models.DecimalField(max_digits=10,decimal_places=2,blank=True,default=0)
    priceSelling=models.DecimalField(max_digits=10,decimal_places=2,blank=True,default=0)
    priceSelling2=models.DecimalField(max_digits=10,decimal_places=2,blank=True,default=0)
    priceSelling3=models.DecimalField(max_digits=10,decimal_places=2,blank=True,default=0)
    tax=models.PositiveIntegerField(blank=True ,default=20)
    currency=models.ForeignKey(currency, on_delete=models.CASCADE, related_name="currency_name")
    stockAmount=models.PositiveIntegerField(default=0)
    photoPath=models.CharField(max_length=1000,blank=True)

    def __str__(self):
        return self.codeUyum

class customer (models.Model):
    customerCode=models.CharField(max_length=50)
    companyName=models.CharField(max_length=50)
    taxOffice=models.CharField(max_length=50)
    tax_number=models.CharField(max_length=50,blank=True)
    name=models.CharField(max_length=50,blank=True)
    middleName=models.CharField(max_length=50,blank=True)
    surname=models.CharField(max_length=50,blank=True)
    city=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
    adress=models.CharField(max_length=250,blank=True)
    country=models.CharField(max_length=50,blank=True, default="Türkiye")
    email=models.EmailField(blank=True)
    telephone=models.CharField(max_length=11,blank=True)
    customerType=models.CharField(max_length=50,blank=True)
    contactPerson=models.CharField(max_length=50,blank=True)
   
    def __str__(self):
        return self.tax_number
class order (models.Model):
    invoiceNumber=models.CharField(max_length=20)
    customer=models.ForeignKey(customer,on_delete=models.CASCADE, related_name="customer_order")
    date=models.DateField()
    product=models.ForeignKey(product,on_delete=models.CASCADE, related_name="product_order")
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2,blank=True,default=0)
    
    def __str__(self):
        return self.invoiceNumber