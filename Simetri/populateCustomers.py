import os
import django
import pandas as pd

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'Simetri.settings'

# Initialize Django
django.setup()

from order.models import Customer


df=pd.read_excel("order/static/customerData.xls")

for index, row in df.iterrows():
    print(f"Customer Code: {row['customerCode']} (Length: {len(str(row['customerCode']))})")
    print(f"Company Name: {row['companyName']} (Length: {len(str(row['companyName']))})")
    print(f"Tax Office: {row['taxOffice']} (Length: {len(str(row['taxOffice']))})")
    print(f"Tax Number: {row['tax_number']} (Length: {len(str(row['tax_number']))})")
    print(f"Name: {row['name']} (Length: {len(str(row['name']))})")
    print(f"Middle Name: {row['middleName']} (Length: {len(str(row['middleName']))})")
    print(f"Surname: {row['surname']} (Length: {len(str(row['surname']))})")
    print(f"City: {row['city']} (Length: {len(str(row['city']))})")
    print(f"District: {row['district']} (Length: {len(str(row['district']))})")
    print(f"Address: {row['adress']} (Length: {len(str(row['adress']))})")
    #print(f"Shipping Address: {row['shipping_adress']} (Length: {len(str(row['shipping_adress']))})")
    print(f"Country: {row['country']} (Length: {len(str(row['country']))})")
    print(f"Email: {row['email']} (Length: {len(str(row['email']))})")
    print(f"Telephone: {row['telephone']} (Length: {len(str(row['telephone']))})")
    print(f"Customer Type: {row['customerType']} (Length: {len(str(row['customerType']))})")
    print(f"Contact Person: {row['contactPerson']} (Length: {len(str(row['contactPerson']))})")

customer_instance = Customer(
    customerCode=row['customerCode'][:50],  # Truncate to 50 characters
    companyName=row['companyName'][:100],  # Truncate to 100 characters
    taxOffice=row['taxOffice'][:50],
    tax_number=row['tax_number'][:50],
    name=row['name'][:100],
    middleName=row['middleName'][:100],
    surname=row['surname'][:100],
    city=row['city'][:50],
    district=row['district'][:50],
    adress=row['adress'][:300],
    shipping_adress=row['shipping_adress'][:300],
    country=row['country'][:50],
    email=row['email'][:100],
    telephone=row['telephone'][:30],
    customerType=row['customerType'][:50],
    contactPerson=row['contactPerson'][:50],
)
customer_instance.save()



