import os
import django
import json

os.environ['DJANGO_SETTINGS_MODULE'] = 'Simetri.settings'
django.setup()

from order.models import location, taxoffice
def populate_locations(data):
    cities = data.get("cities", [])
    tax_offices = data.get("taxOffices", [])
    
    # First, populate locations
    for city_data in cities:
        city_name = city_data.get("cityName", "")
        subdivisions = city_data.get("subdivisions", [])
        
        for sub in subdivisions:
            subdivision_name = sub.get("name", "")
            #location_obj, _ = location.objects.get_or_create(city=city_name, district=subdivision_name, country="Türkiye")
    
    # Then, populate tax offices
    for tax_office_data in tax_offices:
        city_name = tax_office_data.get("city", "")
        vd_name = tax_office_data.get("vdName", "")
        
        
        # Create a TaxOffice object
        tax_office_obj = taxoffice(city=city_name, vd=vd_name)
        tax_office_obj.save()

# Assuming your JSON data is stored in a file named data.json
with open('/Users/ersandagdeviren/Desktop/simetriburoapp/Simetri/order/static/citydata.json') as f:
    data = json.load(f)
    populate_locations(data)
