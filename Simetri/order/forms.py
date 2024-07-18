from django import forms
from .models import Customer, Product , Order, PaymentReceipt
from .models import CustomerUpdateRequest


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
        label='Ürün Ara',
        widget=forms.TextInput(attrs={'placeholder': 'Ürün'})
    )
class ProductaddForm(forms.Form):
    class Meta:
        model = Order
        fields=["invoiceNumber","customer","date","product","quantity","price"]
        
class ProductSessionAddForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1)


class PaymentReceiptForm(forms.ModelForm):
    class Meta:
        model = PaymentReceipt
        fields = ['customer','transaction_type','cash_register',  'expense_item',  'amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].widget.attrs['id'] = 'id_customer'
        self.fields['expense_item'].widget.attrs['id'] = 'id_expense_item'
        self.fields['transaction_type'].widget.attrs['id'] = 'id_transaction_type'
        self.fields['cash_register'].label = 'Kasa'
        self.fields['customer'].label = 'Müşteri'
        self.fields['expense_item'].label = 'Harcama'
        self.fields['transaction_type'].label = 'İşlem Hareketi'
        self.fields['amount'].label = 'Miktar'
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'customerCode',
            'companyName',
            'taxOffice',
            'tax_number',
            'name',
            'middleName',
            'surname',
            'city',
            'district',
            'adress',
            'shipping_adress',
            'country',
            'email',
            'telephone',
            'customerType',
            'contactPerson',
            'E_invoice',
        ]
        widgets = {
            'E_invoice': forms.CheckboxInput(),
        }

class CustomerUpdateRequestForm(forms.ModelForm):
    class Meta:
        model = CustomerUpdateRequest
        fields = ['updated_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['updated_data'].widget = forms.HiddenInput()