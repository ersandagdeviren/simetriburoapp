from django import forms
from .models import customer, product , order


class CustomerForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = ['companyName']

class ProductForm(forms.Form):
    class Meta:
        model= product
        fields = ['description']


class ProductSearchForm(forms.Form):
    product_name = forms.CharField(
        max_length=100,
        label='Search Product',
        widget=forms.TextInput(attrs={'placeholder': 'Ürün'})
    )
class ProductaddForm(forms.Form):
    class Meta:
        model = order
        fields=["invoiceNumber","customer","date","product","quantity","price"]
        
class ProductSessionAddForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1)