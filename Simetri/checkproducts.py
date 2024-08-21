import os
import django
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'Simetri.settings'

# Initialize Django
django.setup()

from order.models import Product  

def export_products_to_excel():
    # Fetch all products
    products = Product.objects.all()

    # Prepare the data for DataFrame
    data = []
    for product in products:
        data.append({
            "Code Uyum": product.codeUyum,
            "Code": product.code,
            "Description": product.description,
            "Unit": product.unit.unit_name,  # Assuming Unit model has 'unit_name' field
            "Status": product.status,
            "Brand": product.brand.brand_name,  # Assuming Brand model has 'brand_name' field
            "Barcode": product.barcode,
            "Main Category": product.mainCategory.mainCategories_name,  # Assuming MainCategory model has 'mainCategories_name'
            "Category": product.category.categories_name,  # Assuming Category model has 'categories_name'
            "Price Selling": product.priceSelling,
            "Price Selling 2": product.priceSelling2,
            "Price Selling 3": product.priceSelling3,
            "Tax": product.tax,
            "Currency": product.currency.currency_name,  # Assuming Currency model has 'currency_name'
            "Photo Path": product.photoPath,
            "Final Product": product.final_product
        })

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Save the DataFrame to an Excel file
    output_path = '/Users/ersandagdeviren/Desktop/productsinmodel.xlsx'
    df.to_excel(output_path, index=False, engine='openpyxl')

    print(f"Data successfully exported to {output_path}")

if __name__ == "__main__":
    export_products_to_excel()
