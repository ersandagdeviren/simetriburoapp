import os
import django
import pandas as pd
from django.conf import settings

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'Simetri.settings'

# Initialize Django
django.setup()

from order.models import Customer

# Construct the correct path to the Excel file using STATIC_ROOT in production
if not settings.DEBUG:
    file_path = os.path.join(settings.STATIC_ROOT, 'customerData.xls')
else:
    # Use the relative path during local development
    file_path = os.path.join('Simetri/order/static/customerData.xls')

# Read the Excel file
df = pd.read_excel(file_path)

# Loop through the rows and create Customer instances
for index, row in df.iterrows():
    customer_instance = Customer(
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
