import os
import django
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'Simetri.settings'

# Initialize Django
django.setup()

from order.models import Product, Place, Inventory

# Read Excel File
df = pd.read_excel('order/static/Inventory.xls')
count = 0

# Iterate Through Rows
for index, row in df.iterrows():
    # Query for the Product instances
    product_instances = Product.objects.filter(codeUyum=row['Product_code'])
    
    # Skip if no products found
    if not product_instances.exists():
        continue

    try:
        # Query for the Place instance
        place_instance = Place.objects.get(name=row['place'])
    except Place.DoesNotExist:
        # Handle the case where the place does not exist
        continue

    for product_instance in product_instances:
        # Get or create an Inventory instance
        inventory_instance, created = Inventory.objects.get_or_create(
            product=product_instance,
            place=place_instance,
            defaults={
                'quantity': row['quantity'],
                'priceBuying': row['price buying']
            }
        )
        count += 1
        print(f'Processed {count} records.')

        if not created:
            # If the inventory record already exists, update the quantity and priceBuying
            inventory_instance.quantity = row['quantity']  # Set quantity directly
            inventory_instance.priceBuying = row['price buying']
            inventory_instance.save()
