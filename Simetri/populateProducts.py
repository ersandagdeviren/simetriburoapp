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
df = pd.read_excel(r'C:\Users\MALIHP\Desktop\simetriburoapp\Simetri\order\static\products.xls')

# Iterate Through Rows
for index, row in df.iterrows():
    try:
        # Query for unit
        unit_instance = unit.objects.get(unitProduct=row['unit'])
    except unit.DoesNotExist:
        # Handle the case where the unit does not exist
        # You can choose to skip this product or handle it differently
        continue
    
    try:
        # Query for brand
        brand_instance = brand.objects.get(brand=row['brand'])
    except brand.DoesNotExist:
        # Handle the case where the brand does not exist
        # You can choose to skip this product or handle it differently
        continue
    
    try:
        # Query for main category
        main_category_instance = mainCategory.objects.get(mainCategory=row['mainCategory'])
    except mainCategory.DoesNotExist:
        # Handle the case where the main category does not exist
        # You can choose to skip this product or handle it differently
        continue
    
    try:
        # Query for category
        category_instance = category.objects.get(category=row['category'])
    except category.DoesNotExist:
        # Handle the case where the category does not exist
        # You can choose to skip this product or handle it differently
        continue

    try:
        # Query for currency
        currency_instance = currency.objects.get(currency=row['currency'])
    except currency.DoesNotExist:
        # Handle the case where the currency does not exist
        # You can choose to skip this product or handle it differently
        continue

    # Create an instance of Product
    product_instance = Product(
        codeUyum=row['codeUyum'],
        code=row['code'],
        description=row['description'],
        unit=unit_instance,
        status=row['status'],
        brand=brand_instance,
        barcode=row['barcode'],
        mainCategory=main_category_instance,
        category=category_instance,
        priceBuying=row['priceBuying'],
        priceSelling=row['priceSelling'],
        priceSelling2=row['priceSelling2'],
        priceSelling3=row['priceSelling3'],
        tax=row['tax'],
        currency=currency_instance,
        #stockAmount=row['stockAmount'],
        photoPath=row['photoPath']
    )

    # Save the instance to the database
    product_instance.save()
