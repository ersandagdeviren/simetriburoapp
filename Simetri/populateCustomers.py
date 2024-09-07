import os
import django
import pandas as pd

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'Simetri.settings'

# Initialize Django
django.setup()

from order.models import Customer


df=pd.read_excel("Simetri/order/static/customerData.xls")

for index, row in df.iterrows():
    customer_instance=Customer(
        customerCode=row['customerCode'],
        companyName=row['companyName'],
        taxOffice=row['taxOffice'],
        tax_number=row['tax_number'],
        name=row['name'],
        surname=row['surname'],
        city=row['city'],
        district=row['district'],
        adress=row['adress'],
        country=row['country'],
        email=row['email'],
        telephone=row['telephone'],
        customerType=row['customerType'],
        contactPerson=row['contactPerson'],

    )
    customer_instance.save()



