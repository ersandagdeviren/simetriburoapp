import os
import django
import pandas as pd

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'Simetri.settings'

# Initialize Django
django.setup()

from order.models import Production, Product

# Read Excel File
df = pd.read_excel('/Users/ersandagdeviren/Desktop/simetriburoapp/Simetri/order/static/production.xls')

# Iterate Through Rows
for index, row in df.iterrows():
    try:
        # Query for product by code
        product_instance = Product.objects.get(codeUyum=row['product'])
    except Product.DoesNotExist:
        # Handle the case where the product does not exist
        continue

    def get_product_by_code(field_name):
        try:
            return Product.objects.get(codeUyum=row[field_name])
        except Product.DoesNotExist:
            return None

    # Create an instance of Production
    production_instance = Production(
        product=product_instance,
        chip=get_product_by_code('chip'),
        empty_cartridge=get_product_by_code('empty_cartridge'),
        cartridge_head=get_product_by_code('cartridge_head'),
        box=get_product_by_code('box'),
        waste_box=get_product_by_code('waste_box'),
        powder=get_product_by_code('powder'),
        powder_gram=row.get('powder_gram', None),
        developer=get_product_by_code('developer'),
        developer_gram=row.get('developer_gram', None)
    )

    # Save the instance to the database
    production_instance.save()
