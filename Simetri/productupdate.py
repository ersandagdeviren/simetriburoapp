import os
import django
import pandas as pd

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'Simetri.settings'

# Initialize Django
django.setup()

from order.models import Product, unit, brand, mainCategory, category, currency

# Read Excel File
df = pd.read_excel(r'C:\Users\MALIHP\Desktop\simetriburoapp\Simetri\order\static\ProductFinal.xls')

# Iterate Through Rows
for index, row in df.iterrows():
    try:
        # Query for related objects (unit, brand, etc.)
        unit_instance = unit.objects.get(unitProduct=row['unit'])
        brand_instance = brand.objects.get(brand=row['brand'])
        main_category_instance = mainCategory.objects.get(mainCategory=row['mainCategory'])
        category_instance = category.objects.get(category=row['category'])
        currency_instance = currency.objects.get(currency=row['currency'])

        # Try to filter products by 'codeUyum'
        product_queryset = Product.objects.filter(codeUyum=row['codeUyum'])

        if product_queryset.exists():
            # Update all matching products
            for product_instance in product_queryset:
                product_instance.priceSelling = row['priceSelling']
                product_instance.priceSelling2 = row['priceSelling2']
                product_instance.priceSelling3 = row['priceSelling3']
                # Update any other fields that need to be updated
                product_instance.save()
        else:
            # If no product exists, create a new one
            Product.objects.create(
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

    except unit.DoesNotExist:
        print(f"Unit does not exist for row {index}, skipping...")
    except brand.DoesNotExist:
        print(f"Brand does not exist for row {index}, skipping...")
    except mainCategory.DoesNotExist:
        print(f"Main Category does not exist for row {index}, skipping...")
    except category.DoesNotExist:
        print(f"Category does not exist for row {index}, skipping...")
    except currency.DoesNotExist:
        print(f"Currency does not exist for row {index}, skipping...")
    except Exception as e:
        print(f"An error occurred while processing row {index}: {e}")
