import os
import django
import pandas as pd

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'Simetri.settings'

# Initialize Django
django.setup()

from order.models import location
from django.core.exceptions import ObjectDoesNotExist

# Read Excel File
df = pd.read_excel('/Users/ersandagdeviren/Desktop/simetriburoapp/Simetri/order/static/city.xls')

# Iterate Through Rows
for index, row in df.iterrows():
    location_instance=location(
        city=row['city'],
        country=row['country']
    )
    location_instance.save()
   







