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
df = pd.read_excel("order/static/productFinal.xls")

# Check for duplicate codeUyum values in the Excel file
duplicated_codes = df[df.duplicated(subset=['codeUyum'], keep=False)]

# Print out the duplicated codeUyum values in a table format
if not duplicated_codes.empty:
    print("Duplicated codeUyum values in the Excel file:")
    print(duplicated_codes[['codeUyum', 'description']].to_string(index=False))
else:
    print("No duplicated codeUyum values found in the Excel file.")

# Iterate Through Rows
for index, row in df.iterrows():
    try:
        # Query for unit
        unit_instance = unit.objects.get(unitProduct=row['unit'])
    except unit.DoesNotExist:
        print(f"Unit '{row['unit']}' does not exist for product: {row['codeUyum']}")
        continue

    try:
        # Query for brand
        brand_instance = brand.objects.get(brand=row['brand'])
    except brand.DoesNotExist:
        print(f"Brand '{row['brand']}' does not exist for product: {row['codeUyum']}")
        continue

    try:
        # Query for main category
        main_category_instance = mainCategory.objects.get(mainCategory=row['mainCategory'])
    except mainCategory.DoesNotExist:
        print(f"Main Category '{row['mainCategory']}' does not exist for product: {row['codeUyum']}")
        continue

    try:
        # Query for category
        category_instance = category.objects.get(category=row['category'])
    except category.DoesNotExist:
        print(f"Category '{row['category']}' does not exist for product: {row['codeUyum']}")
        continue

    try:
        # Query for currency
        currency_instance = currency.objects.get(currency=row['currency'])
    except currency.DoesNotExist:
        print(f"Currency '{row['currency']}' does not exist for product: {row['codeUyum']}")
        continue

    # Try to retrieve the product by its unique identifier (e.g., code or codeUyum)
    try:
        product_instance = Product.objects.get(codeUyum=row['codeUyum'])
        # If the product exists, update the relevant fields
        product_instance.priceSelling = row['priceSelling']
        product_instance.priceSelling2 = row['priceSelling2']
        product_instance.priceSelling3 = row['priceSelling3']
        product_instance.description = row['description']
        product_instance.unit = unit_instance
        product_instance.status = row['status']
        product_instance.brand = brand_instance
        product_instance.barcode = row['barcode']
        product_instance.mainCategory = main_category_instance
        product_instance.category = category_instance
        product_instance.tax = row['tax']
        product_instance.currency = currency_instance
        product_instance.photoPath = row['photoPath']
        product_instance.final_product = row['final_product']
        
    except Product.DoesNotExist:
        # If the product does not exist, create a new one
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
            priceSelling=row['priceSelling'],
            priceSelling2=row['priceSelling2'],
            priceSelling3=row['priceSelling3'],
            tax=row['tax'],
            currency=currency_instance,
            photoPath=row['photoPath'],
            final_product=row['final_product']
        )

    try:
        # Save the instance (whether updated or newly created) to the database
        product_instance.save()
    except Exception as e:
        print(f"Failed to save product '{row['codeUyum']}': {e}")
