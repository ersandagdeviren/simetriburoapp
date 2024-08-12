import os
import django
import pandas as pd

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'Simetri.settings'

# Initialize Django
django.setup()

from order.models import Product, unit, brand, mainCategory, category, currency
from django.core.exceptions import ObjectDoesNotExist

# Read Excel File
df = pd.read_excel('/Users/ersandagdeviren/Desktop/simetriburoapp/Simetri/order/static/productsson.xls')

# Iterate Through Rows
for index, row in df.iterrows():
    try:
        # Find the product by its unique identifier (codeUyum in this case)
        product_instance = Product.objects.get(codeUyum=row['codeUyum'])

        # Update the photoPath
        product_instance.photoPath = row['photoPath']

        # Save the changes to the database
        product_instance.save()
        
    except Product.DoesNotExist:
        # Handle the case where the product does not exist
        print(f"Product with codeUyum {row['codeUyum']} does not exist in the database.")
        continue