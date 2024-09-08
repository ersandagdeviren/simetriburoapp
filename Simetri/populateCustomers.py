import os
import django
import pandas as pd

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'Simetri.settings'

# Initialize Django
django.setup()

from order.models import Customer

# Load data from the Excel file
df = pd.read_excel("order/static/customerData.xls")

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Print the length of each field
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
    print(f"Country: {row['country']} (Length: {len(str(row['country']))})")
    print(f"Email: {row['email']} (Length: {len(str(row['email']))})")
    print(f"Telephone: {row['telephone']} (Length: {len(str(row['telephone']))})")
    print(f"Customer Type: {row['customerType']} (Length: {len(str(row['customerType']))})")
    print(f"Contact Person: {row['contactPerson']} (Length: {len(str(row['contactPerson']))})")

    # Check if the customer already exists based on customerCode or email
    if Customer.objects.filter(customerCode=row['customerCode']).exists():
        print(f"Skipping existing customer: {row['customerCode']}")
        continue  # Skip this customer if they already exist

    # Create and save the customer instance
    customer_instance = Customer(
        customerCode=row['customerCode'], # Truncate to 50 characters
        companyName=row['companyName'][:100],  # Truncate to 100 characters
        taxOffice=row['taxOffice'],
        tax_number=row['tax_number'],
        name=row['name'][:100],
        middleName=row['middleName'],
        surname=row['surname'],
        city=row['city'],
        district=row['district'],
        adress=row['adress'][:300],
        country=row['country'][:50],
        email=row['email'],
        telephone=row['telephone'],
        customerType=row['customerType'],
        contactPerson=row['contactPerson'],
    )
    customer_instance.save()
