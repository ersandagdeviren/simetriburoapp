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



