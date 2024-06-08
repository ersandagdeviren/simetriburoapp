from django import forms
from .models import Customer, Product , Order


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['companyName']

class ProductForm(forms.Form):
    class Meta:
        model= Product
        fields = ['description']


class ProductSearchForm(forms.Form):
    product_name = forms.CharField(
        max_length=100,
        label='Search Product',
        widget=forms.TextInput(attrs={'placeholder': 'Ürün'})
    )
class ProductaddForm(forms.Form):
    class Meta:
        model = Order
        fields=["invoiceNumber","customer","date","product","quantity","price"]
        
class ProductSessionAddForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1)