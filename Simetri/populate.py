import os
import django
import pandas as pd

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'Simetri.settings'

# Initialize Django
django.setup()

from order.models import location, taxOffice
from django.core.exceptions import ObjectDoesNotExist

# Read Excel File
df = pd.read_excel('/Users/ersandagdeviren/Documents/GitHub/simetriapp/Simetri/order/static/taxx.xls')

# Iterate Through Rows
for index, row in df.iterrows():
    # Assuming 'city_column' is the column containing Location (ForeignKey) values in the Excel file
    city_name = row['city']

    # Retrieve the related Location object
    try:
        location_instance = location.objects.get(city=city_name)
    except ObjectDoesNotExist:
        # Handle the case where the related Location object does not exist
        print(f"Location with city '{city_name}' does not exist.")
        continue

    # Create an instance of TaxOffice with the ForeignKey relationship
    tax_office_instance = taxOffice(
        taxOffice=row['taxOffice'],
        city=location_instance,
    )

    # Save the instance to the database
    tax_office_instance.save()









'''

the code below from got from chapGPT



import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Simetri.settings'
import django
django.setup()
from django_xlspopulator.populator import Populator
from order.models import location ,taxOffice




def taxpopulate():
    url = '/Users/ersandagdeviren/Documents/GitHub/simetriapp/Simetri/order/static/taxx.xls'
    pop = Populator(url, taxOffice)
    pop.populate()



if __name__ == '__main__':
    print("populating string")
    taxpopulate()

    print("completed")

    '''