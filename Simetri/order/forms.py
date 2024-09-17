from django import forms
from .models import Customer, Product , Order, PaymentReceipt, Production, Supplier,CashRegister,ExpenseItem
from .models import CustomerUpdateRequest
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
import random

User = get_user_model()


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
        fields = ['customer', 'supplier', 'transaction_type', 'cash_register', 'expense_item', 'amount', 'usd_amount', 'eur_amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Kaydet'))
        self.fields['customer'].widget.attrs['id'] = 'id_customer'
        self.fields['expense_item'].widget.attrs['id'] = 'id_expense_item'
        self.fields['transaction_type'].widget.attrs['id'] = 'id_transaction_type'
        self.fields['cash_register'].label = 'Kasa'
        self.fields['customer'].label = 'Müşteri'
        self.fields['expense_item'].label = 'Harcama'
        self.fields['transaction_type'].label = 'İşlem Hareketi'
        self.fields['amount'].label = 'TL Tutar'
        self.fields['supplier'].label = 'Tedarikçi'
        self.fields['usd_amount'].label = 'USD Tutarı'
        self.fields['eur_amount'].label = 'EUR Tutarı'
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            # 'customerCode',  # Removed from the form fields to be hidden
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
            # 'customerType',  # Removed from the form fields to be hidden
            'contactPerson',
            'E_invoice',
        ]
        labels = {
            'companyName': 'Firma Ünvanı',
            'taxOffice': 'Vergi Dairesi',
            'tax_number': 'Vergi Numarası',
            'name': 'Ad',
            'middleName': 'Orta Ad',
            'surname': 'Soyad',
            'city': 'Şehir',
            'district': 'İlçe',
            'adress': 'Adres',
            'shipping_adress': 'Kargo Adresi',
            'country': 'Ülke',
            'email': 'Fatura E Posta adresi',
            'telephone': 'Telefon',
            'contactPerson': 'İlgili Kişi',
            'E_invoice': 'E Fatura Mükellefi',
        }
        widgets = {
            'adress': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),  # Make adress larger
            'shipping_adress': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),  # Make shipping_adress larger
            'E_invoice': forms.CheckboxInput(),
        }

    # Automatically generate a 6-digit customerCode
    def save(self, commit=True):
        instance = super(CustomerForm, self).save(commit=False)
        if not instance.customerCode:
            instance.customerCode = random.randint(100000, 999999)  # Generate a 6-digit number
        if commit:
            instance.save()
        return instance
class CustomerUpdateRequestForm(forms.ModelForm):
    class Meta:
        model = CustomerUpdateRequest
        fields = ['updated_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['updated_data'].widget = forms.HiddenInput()

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"

class TransferForm(forms.Form):
    source_register = forms.ModelChoiceField(queryset=CashRegister.objects.all())
    target_register = forms.ModelChoiceField(queryset=CashRegister.objects.all())
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    fee = forms.DecimalField(max_digits=10, decimal_places=2)
    expense_item = forms.ModelChoiceField(queryset=ExpenseItem.objects.all())

class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': "E Posta Adresi",
            'email': 'E Posta Adresi (onay)',
            'password1': "Şifre",
            'password2': 'Şifre Tekrar'
        }