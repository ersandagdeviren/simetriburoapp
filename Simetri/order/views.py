from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django import forms
from django.utils import timezone
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from order.models import Product, Customer, Order, OrderItem, Invoice,CashRegister,ExpenseItem,PaymentReceipt, CustomerUpdateRequest, Place,Production, Inventory, Transfer,Production,Supplier,BuyingInvoice,BuyingItem,CashRegister,Transaction,mainCategory,category
from .forms import ProductSearchForm ,PaymentReceiptForm,CustomerForm, CustomerUpdateRequestForm,SupplierForm,TransferForm,CustomerSignUpForm
from decimal import Decimal, ROUND_HALF_UP
from django.http import JsonResponse
import datetime
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import NoSuchElementException ,TimeoutException
from .forms import ProductForm 
from selenium.webdriver.chrome.service import Service






"""
    webpage_response = requests.get('https://canlidoviz.com/doviz-kurlari/garanti-bankasi')
    webpage = webpage_response.content
    soup = BeautifulSoup(webpage, "html.parser")
    target_data_usd = soup.select_one("html > body > div:nth-of-type(3) > div > div:nth-of-type(3) > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(4) > table > tbody > tr:nth-of-type(1) > td:nth-of-type(3) > div > span").get_text()
    target_data_usd = Decimal(str(target_data_usd).replace(" ", "").replace("\n", "")).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    target_data_eur = soup.select_one("html > body > div:nth-of-type(3) > div > div:nth-of-type(3) > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(4) > table > tbody > tr:nth-of-type(2) > td:nth-of-type(3) > div > span").get_text()
    target_data_eur = Decimal(str(target_data_eur).replace(" ", "").replace("\n", "")).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
"""


def get_currency_rates():

    webpage_response2 = requests.get('https://www.altinkaynak.com/Doviz/Kur/Guncel')
    webpage2 = webpage_response2.content
    soup2 = BeautifulSoup(webpage2, "html.parser")
    target_data_usd = round(float(soup2.find(id="tdUSDSell").get_text().replace(",", ".")), 2)
    target_data_eur= round(float(soup2.find(id="tdEURSell").get_text().replace(",", ".")), 2)
    return target_data_usd, target_data_eur

def is_admin(user):
    return user.is_authenticated and user.is_staff

def customer_details(request, id):
    customer = get_object_or_404(Customer, id=id)
    return render(request, 'order/customer_details.html', {'customer': customer})

@login_required
def search(request):
    form = ProductSearchForm(request.POST or None)
    query = ''
    productresult = None

    if request.method == "POST" and form.is_valid():
        query = form.cleaned_data["product_name"]

        if query:
            # Split the query into individual words
            query_words = query.split()
            # Create a Q object to combine conditions
            q_objects = Q()
            for word in query_words:
                # Update the Q object with each word
                q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)
            
            # Filter products based on the Q object
            productresult = Product.objects.filter(q_objects)

            # Retrieve stock amount from Inventory for both "D1" and "D4"
            for product in productresult:
                inventory_d1 = Inventory.objects.filter(product=product, place__name="D1").first()
                inventory_d4 = Inventory.objects.filter(product=product, place__name="D4").first()
                product.stockAmountD1 = inventory_d1.quantity if inventory_d1 else 0
                product.stockAmountD4 = inventory_d4.quantity if inventory_d4 else 0

    # Remove pagination logic, simply pass the full list
    return render(request, "order/product.html", {"form": form, "productresult": productresult, "query": query})

@login_required
def main(request):
    try:
        webpage_response = requests.get('https://canlidoviz.com/doviz-kurlari/garanti-bankasi')
        webpage = webpage_response.content
        soup = BeautifulSoup(webpage, "html.parser")
        target_data_usd = soup.select_one(
            "body > div.flex.w-full.justify-center.px-3 > div > div.flex.flex-col.sc1300\:flex-row.justify-center.max-w-\[1500px\].gap-3.min-w-0 > div > div.flex.gap-3.w-full.flex-col.lg\:flex-row > div.w-full > div.flex.lg\:px-3.flex-col.flex-\[1_1_auto\].lg\:bg-pholder.lg\:theme-dark\:bg-dPholder.lg\:theme-light\:bg-wPholder.shadow-boxShadow > div.py-0 > table > tbody > tr:nth-child(1) > td.align-middle.md\:align-top.text-right.w-24.truncate.ml-6 > div").get_text()
        target_data_usd = round(float(str(target_data_usd).replace(" ", "").replace("\n", "")[:5]), 2)
        target_data_usd = round(target_data_usd, 2)  # Keep it as a float for now

        target_data_eur = soup.select_one(
            "body > div.flex.w-full.justify-center.px-3 > div > div.flex.flex-col.sc1300\:flex-row.justify-center.max-w-\[1500px\].gap-3.min-w-0 > div > div.flex.gap-3.w-full.flex-col.lg\:flex-row > div.w-full > div.flex.lg\:px-3.flex-col.flex-\[1_1_auto\].lg\:bg-pholder.lg\:theme-dark\:bg-dPholder.lg\:theme-light\:bg-wPholder.shadow-boxShadow > div.py-0 > table > tbody > tr:nth-child(2) > td.align-middle.md\:align-top.text-right.w-24.truncate.ml-6 > div").get_text()
        target_data_eur = round(float(str(target_data_eur).replace(" ", "").replace("\n", "")[:5]), 2)
        target_data_eur = round(target_data_eur, 2)  # Keep it as a float for now
    except:
        target_data_usd=0
        target_data_eur=0

        
    try:
        webpage_response2 = requests.get('https://www.altinkaynak.com/Doviz/Kur/Guncel')
        webpage2 = webpage_response2.content
        soup2 = BeautifulSoup(webpage2, "html.parser")
        target_data_usd2 = round(float(soup2.find(id="tdUSDSell").get_text().replace(",", ".")), 2)
        target_data_usd2 = round(target_data_usd2, 2)  # Keep it as a float for now

        target_data_eur2 = round(float(soup2.find(id="tdEURSell").get_text().replace(",", ".")), 2)
        target_data_eur2 = round(target_data_eur2, 2)  # Keep it as a float for now
    except:
        target_data_usd2=0
        target_data_eur2=0
        
    today = datetime.date.today()
    orders = Order.objects.filter(date__gt=today)
    orders_with_totals = []

    for order in orders:
        total_amount_usd = 0
        total_amount_eur = 0
        total_amount_tl = 0
        total_tax = 0
        total_discount = 0

        for item in order.order_items.all():
            product = item.product
            if item.discount_rate == 0:
                price_in_tl = item.price * item.quantity * item.currency_rate
                discount = 0
            else:
                price_in_tl = item.price * (100 - item.discount_rate) / 100 * item.quantity * item.currency_rate
                discount = (item.price * item.quantity * item.currency_rate) - (item.price * (100 - item.discount_rate) / 100 * item.quantity * item.currency_rate)
            product_tax = price_in_tl * product.tax / 100

            if str(product.currency) == 'USD':
                total_amount_usd += item.price * item.quantity
            else:  # Assuming it's EUR if not USD
                total_amount_eur += item.price * item.quantity

            total_amount_tl += price_in_tl
            total_tax += product_tax
            total_discount += discount

        total_amount_tl = round(total_amount_tl, 2)
        total_amount_eur = round(total_amount_eur, 2)
        total_amount_usd = round(total_amount_usd, 2)
        total_discount = round(total_discount, 2)
        total_tax = round(total_tax, 2)
        grand_total = total_amount_tl + total_tax

        orders_with_totals.append({
            'order': order,
            'total_amount_usd': total_amount_usd,
            'total_amount_eur': total_amount_eur,
            'total_amount_tl': total_amount_tl,
            'total_discount': total_discount,
            'total_tax': total_tax,
            'grand_total': grand_total,
            'order_date': order.date.strftime('%d-%m-%Y'),  # Adding the order date
        })

    # Format the numbers with thousand separators just before rendering
    for order in orders_with_totals:
        order['total_amount_usd'] = f"{order['total_amount_usd']:,.2f}"
        order['total_amount_eur'] = f"{order['total_amount_eur']:,.2f}"
        order['total_amount_tl'] = f"{order['total_amount_tl']:,.2f}"
        order['total_discount'] = f"{order['total_discount']:,.2f}"
        order['total_tax'] = f"{order['total_tax']:,.2f}"
        order['grand_total'] = f"{order['grand_total']:,.2f}"

    target_data_usd = f"{target_data_usd:,.2f}"
    target_data_eur = f"{target_data_eur:,.2f}"
    target_data_usd2 = f"{target_data_usd2:,.2f}"
    target_data_eur2 = f"{target_data_eur2:,.2f}"

    invoices = Invoice.objects.all().order_by('-invoice_date')
    invoices = invoices.filter(invoice_date__gt=today)
    payment_receipts = PaymentReceipt.objects.all().filter(date__gt=today)

    return render(request, "order/index.html", {
        "target_data_usd": target_data_usd,
        "target_data_eur": target_data_eur,
        "target_data_usd2": target_data_usd2,
        "target_data_eur2": target_data_eur2,
        "orders_with_totals": orders_with_totals,
        'invoices': invoices,
        'payment_receipts': payment_receipts,
    })


@login_required
def comparison(request):
    return render(request, "order/comparison.html")

@login_required
@user_passes_test(is_admin)
def customer_list(request):
    if "customers" not in request.session:
        request.session["customers"] = []
    if "products" not in request.session:
        request.session["products"] = []
    if "product_query" not in request.session:
        request.session["product_query"] = ""

    customer_list = []
    customer_selected = request.session['customers']
    product_form = ProductSearchForm(request.POST or None)
    productresult = []  # Initialize productresult

    if request.method == "POST" and "customer_searched" in request.POST:
        input_customer = request.POST.get('customer')
        customer_list = Customer.objects.filter(companyName__icontains=input_customer)
        if not customer_list:
            messages.info(request, 'No customers found matching your search.')
        return render(request, 'order/order_create.html', {
            "customer_list": customer_list,
            "customer_selected": customer_selected,
        })

    elif request.method == "POST" and "customer_selected" in request.POST:
        request.session['customers'] = []
        customer_id = request.POST.get('customer_id')
        customer_name = Customer.objects.get(id=customer_id).companyName
        request.session['customers'].append(customer_id)
        return render(request, 'order/order_create.html', {
            "customer_name": customer_name,
            "product_form": product_form,
            "products": request.session['products']
        })

    elif request.method == "POST" and "product_submit" in request.POST:
        customer_name = Customer.objects.get(id=request.session['customers'][0]).companyName
        if product_form.is_valid():
            query = product_form.cleaned_data["product_name"]
            request.session['product_query'] = query  # Store the search query in the session
            if query:
                # Split the query into individual words
                query_words = query.split()
                # Create a Q object to combine conditions
                q_objects = Q()
                for word in query_words:
                    # Update the Q object with each word
                    q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)
                
                # Filter products based on the Q object
                productresult = Product.objects.filter(q_objects)

                # Retrieve stock amount from Inventory where place is "D1"
                for product in productresult:
                    inventory = Inventory.objects.filter(product=product, place__name="D1").first()
                    product.stockAmount = inventory.quantity if inventory else 0

                return render(request, 'order/order_create.html', {
                    "product_form": product_form,
                    "product": productresult,
                    "customer_name": customer_name,
                    "products": request.session['products']
                })

    elif request.method == "POST" and "product_add" in request.POST:
        product_id = request.POST.get('item_id')
        new_price = request.POST.get('new_price')
        quantity = request.POST.get('quantity')
        description = Product.objects.get(id=product_id).description
        currency = Product.objects.get(id=product_id).currency

        if str(currency) == 'USD':
            currency_rate = float(get_currency_rates()[0])
        if str(currency) == 'EUR':
            currency_rate = float(get_currency_rates()[1])

        product_entry = {
            'id': product_id,
            'price': new_price,
            'quantity': quantity,
            'description': description,
            'currency_rate': currency_rate
        }

        products = request.session.get('products', [])
        products.append(product_entry)
        request.session['products'] = products

        customer_name = Customer.objects.get(id=request.session['customers'][0]).companyName

        query = request.session.get('product_query', "")
        if query:
            # Split the query into individual words
            query_words = query.split()
            # Create a Q object to combine conditions
            q_objects = Q()
            for word in query_words:
                # Update the Q object with each word
                q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)
            
            # Filter products based on the Q object
            productresult = Product.objects.filter(q_objects)

            # Retrieve stock amount from Inventory where place is "D1"
            for product in productresult:
                inventory = Inventory.objects.filter(product=product, place__name="D1").first()
                product.stockAmount = inventory.quantity if inventory else 0

        return render(request, 'order/order_create.html', {
            "product_form": product_form,
            "customer_name": customer_name,
            "products": request.session['products'],
            "product": productresult
        })

    elif request.method == "POST" and "delete_product" in request.POST:
        product_id = request.POST.get('product_id')
        products = request.session.get('products', [])
        products = [product for product in products if product['id'] != product_id]
        request.session['products'] = products

        customer_name = Customer.objects.get(id=request.session['customers'][0]).companyName

        query = request.session.get('product_query', "")
        if query:
            # Split the query into individual words
            query_words = query.split()
            # Create a Q object to combine conditions 
            q_objects = Q()
            for word in query_words:
                # Update the Q object with each word
                q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)
            
            # Filter products based on the Q object
            productresult = Product.objects.filter(q_objects)

            # Retrieve stock amount from Inventory where place is "D1"
            for product in productresult:
                inventory = Inventory.objects.filter(product=product, place__name="D1").first()
                product.stockAmount = inventory.quantity if inventory else 0

        return render(request, 'order/order_create.html', {
            "product_form": product_form,
            "customer_name": customer_name,
            "products": request.session['products'],
            "product": productresult
        })

    elif request.method == "POST" and "complete_order" in request.POST:
        customer_id = request.session.get('customers')[0]
        product_ids = [item['id'] for item in request.session.get('products', [])]
        quantities = [item['quantity'] for item in request.session.get('products', [])]
        prices = [item['price'] for item in request.session.get('products', [])]
        currencies = [item['currency_rate'] for item in request.session.get('products', [])]

        order = Order.objects.create(customer_id=customer_id, user=request.user)

        for product_id, quantity, price, currency_rate in zip(product_ids, quantities, prices, currencies):
            OrderItem.objects.create(order=order, product_id=product_id, quantity=quantity, price=price, currency_rate=currency_rate, discount_rate=0)

        request.session['products'] = []
        request.session['customers'] = []
        request.session['product_query'] = ""
        return redirect('order:order_detail', order_number=order.order_number)

       
    else:
        return render(request, 'order/order_create.html', {
            "product_form": product_form,
            "customer_selected": customer_selected,
        })


def create_order(request):
    if request.method == 'POST':
        # Handling product search
        if 'product_submit' in request.POST:
            product_form = ProductForm(request.POST)
            if product_form.is_valid():
                product_name = product_form.cleaned_data['product_name']
                # Fetching products that match the search criteria
                products = Product.objects.filter(name__icontains=product_name)
            else:
                products = Product.objects.none()  # No products if form is invalid
        else:
            products = Product.objects.none()

        # Handling adding products to the cart
        if 'product_add' in request.POST:
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity', 1))

            product = Product.objects.get(id=item_id)
            inventory = Inventory.objects.filter(product=product, place__name="D1").first()
            if inventory and inventory.quantity >= quantity:
                # Logic to add product to cart, e.g., save to session or database
                messages.success(request, f'Added {quantity} of {product.name} to the cart.')
            else:
                messages.error(request, 'Not enough stock available.')

        # Handling deleting products from the cart
        if 'delete_product' in request.POST:
            product_id = request.POST.get('product_id')
            # Logic to remove product from cart, e.g., update session or database
            messages.success(request, f'Removed product with ID {product_id} from the cart.')

        # Handling completing the order
        if 'complete_order' in request.POST:
            # Logic to complete the order, e.g., save order and redirect
            messages.success(request, 'Order completed successfully.')
            return redirect('order:order_list')

        # Handling form submission for price, quantity, etc.
        if 'product_form' in request.POST:
            # Fetching products for display
            product_form = ProductForm()
            products = Product.objects.all()

        else:
            product_form = ProductForm()
            products = Product.objects.all()

    else:
        # Initial GET request
        product_form = ProductForm()
        products = Product.objects.all()

    # Prepare inventory data for template
    inventory_dict = {}
    for product in products:
        inventory = Inventory.objects.filter(product=product, place__name="D1").first()
        if inventory:
            inventory_dict[product.id] = inventory.quantity
        else:
            inventory_dict[product.id] = 0

    context = {
        'products': products,
        'product_form': product_form,
        'inventory_dict': inventory_dict,
    }
    return render(request, 'order/create_order.html', context)

@login_required
@user_passes_test(is_admin)
def order_list(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        return redirect('order:order_list')

    orders = Order.objects.all().order_by('-date')
    orders_with_totals = []

    for order in orders:
        total_amount_usd = 0
        total_amount_eur = 0
        total_amount_tl = 0
        total_tax = 0
        total_discount = 0

        for item in order.order_items.all():
            product = item.product
            if item.discount_rate == 0:
                price_in_tl = item.price * item.quantity * item.currency_rate
                discount = 0
            else:
                price_in_tl = item.price * (100 - item.discount_rate) / 100 * item.quantity * item.currency_rate
                discount = (item.price * item.quantity * item.currency_rate) - (
                        item.price * (100 - item.discount_rate) / 100 * item.quantity * item.currency_rate)
            product_tax = price_in_tl * product.tax / 100

            if str(product.currency) == 'USD':
                total_amount_usd += item.price * item.quantity
            else:  # Assuming it's EUR if not USD
                total_amount_eur += item.price * item.quantity

            total_amount_tl += price_in_tl
            total_tax += product_tax
            total_discount += discount

        total_amount_tl = round(total_amount_tl, 2)
        total_amount_eur = round(total_amount_eur, 2)
        total_amount_usd = round(total_amount_usd, 2)
        total_discount = round(total_discount, 2)
        total_tax = round(total_tax, 2)
        grand_total = total_amount_tl + total_tax

        orders_with_totals.append({
            'order': order,
            'total_amount_usd': f"{total_amount_usd:,.2f}",
            'total_amount_eur': f"{total_amount_eur:,.2f}",
            'total_amount_tl': f"{total_amount_tl:,.2f}",
            'total_discount': f"{total_discount:,.2f}",
            'total_tax': f"{total_tax:,.2f}",
            'grand_total': f"{grand_total:,.2f}",
            'order_date': order.date.strftime('%d-%m-%Y'),  # Adding the order date
        })

    # No pagination, just pass the full list
    return render(request, 'order/order_list.html', {'orders_with_totals': orders_with_totals})

@login_required
def order_detail(request, order_number):
    defaultUSD, defaultEUR = get_currency_rates()
    order = get_object_or_404(Order, order_number=order_number)
    if order.customer.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this info.")
    
    product_form = ProductSearchForm(request.POST or None)
    productresult = None

    if request.method == 'POST':
        if 'product_submit' in request.POST:
            if product_form.is_valid():
                query = product_form.cleaned_data.get("product_name", "")
                if query:
                    # Split the query into individual words
                    query_words = query.split()
                    # Create a Q object to combine conditions
                    q_objects = Q()
                    for word in query_words:
                        # Update the Q object with each word
                        q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)
                    
                    # Filter products based on the Q object
                    productresult = Product.objects.filter(q_objects)

                    # Retrieve stock amount from Inventory where place is "D1"
                    for product in productresult:
                        inventory = Inventory.objects.filter(product=product, place__name="D1").first()
                        product.stockAmount = inventory.quantity if inventory else 0

                    # Format numerical values with thousand separators
                    for product in productresult:
                        product.stockAmount = f"{product.stockAmount:,.2f}"
                else:
                    productresult = []
        elif 'delete_item' in request.POST:
            item_id = request.POST.get('delete_item')
            item = get_object_or_404(OrderItem, id=item_id, order=order)
            item.delete()
            return redirect('order:order_detail', order_number=order.order_number)
        
        elif 'product_add' in request.POST:
            product_id = request.POST.get('item_id')
            new_price = request.POST.get('new_price')
            
            quantity = request.POST.get('quantity')
            product = get_object_or_404(Product, id=product_id)
            currency = product.currency

            if str(currency) == 'USD':
                currency_rate = float(defaultUSD)
            elif str(currency) == 'EUR':
                currency_rate = float(defaultEUR)
            else:
                currency_rate = 1

            order_item = OrderItem(
                order=order,
                product=product,
                quantity=int(quantity),
                price=float(new_price),
                currency_rate=currency_rate,
            )
            order_item.save()
            return redirect('order:order_detail', order_number=order.order_number)

        elif 'update' in request.POST:
            for item in order.order_items.all():
                quantity = request.POST.get(f'quantity_{item.id}')
                price = request.POST.get(f'price_{item.id}')
                currency_rate = request.POST.get(f'currency_rate_{item.id}')
                discount_rate = request.POST.get(f'discount_rate_{item.id}')

                if quantity is not None and price is not None and currency_rate is not None and discount_rate is not None:
                    item.quantity = int(quantity)
                    item.price = float(price)
                    item.currency_rate = float(currency_rate)
                    item.discount_rate = float(discount_rate)
                    item.save()
            return redirect('order:order_detail', order_number=order.order_number)
        
        elif 'update_user' in request.POST:
            for item in order.order_items.all():
                quantity = request.POST.get(f'quantity_{item.id}')
                if quantity is not None:
                    item.quantity = int(quantity)
                    item.save()
            return redirect('order:order_detail', order_number=order.order_number)

    order_items_with_tl = []
    total_amount = 0
    total_discount = 0
    total_tax = 0
    grand_total = 0

    for item in order.order_items.all():
        currency_rate = item.currency_rate
        discount_amount = item.price * item.discount_rate / 100
        tl_value = round((item.price - discount_amount) * currency_rate * item.quantity, 2)
        item_tax = round(tl_value * item.product.tax / 100, 2)
        item_total = tl_value + item_tax

        total_amount += tl_value
        total_tax += item_tax
        total_discount += round(discount_amount * item.quantity * currency_rate, 2)
        grand_total = total_amount + total_tax

        order_items_with_tl.append({
            'item': item,
            'tl_value': tl_value,
            'currency_rate': currency_rate,
            'tax': item_tax,    
            'total': item_total,
            'discount_rate': item.discount_rate
        })

    return render(request, 'order/order_detail.html', {
        'order': order,
        'total_amount': total_amount,
        'total_tax': total_tax,
        'total_discount': total_discount,
        'order_items_with_tl': order_items_with_tl,
        'grand_total': grand_total,
        'product_form': product_form,
        'productresult': productresult,
    })
@login_required
@user_passes_test(is_admin)
def create_invoice(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    # Check if an invoice already exists for the order
    if hasattr(order, 'invoice'):
        messages.error(request, 'Invoice already exists for this order.')
        return redirect('order:order_detail', order_number=order_number)
    
    # Check stock for each item in the order from Inventory where place is "D1"
    for item in order.order_items.all():
        inventory = Inventory.objects.filter(product=item.product, place__name="D1").first()
        stock_amount = inventory.quantity if inventory else 0
        if stock_amount < item.quantity:
            messages.error(request, f"Not enough stock for product {item.product.description}.")
            return redirect('order:order_detail', order_number=order_number)

    total_amount = 0
    total_discount = 0
    total_tax = 0
    grand_total = 0
    usd_total_amount = 0
    usd_total_discount = 0
    usd_total_tax = 0
    grand_total_USD = 0
    eur_total_amount = 0
    eur_total_discount = 0
    eur_total_tax = 0
    grand_total_EUR = 0

    for item in order.order_items.all():
        if str(item.product.currency) == 'USD':
            usd_value = round((item.price - (item.price * item.discount_rate / 100)) * item.quantity, 2)
            usd_discount_value = (item.price * item.discount_rate / 100)
            usd_tax_value = round(usd_value * item.tax / 100, 2)
        else:
            usd_value = 0
            usd_discount_value = 0
            usd_tax_value = 0

        if str(item.product.currency) == 'EUR':
            eur_value = round((item.price - (item.price * item.discount_rate / 100)) * item.quantity, 2)
            eur_discount_value = (item.price * item.discount_rate / 100)
            eur_tax_value = round(eur_value * item.tax / 100, 2)
        else:
            eur_value = 0
            eur_discount_value = 0
            eur_tax_value = 0

        tl_value = round((item.price - (item.price * item.discount_rate / 100)) * item.currency_rate * item.quantity, 2)
        discount_value_tl = (item.price * item.discount_rate / 100) * item.currency_rate
        tax_value_tl = round(tl_value * item.tax / 100, 2)

        total_amount += tl_value
        total_tax += tax_value_tl
        total_discount += discount_value_tl
        
        usd_total_amount += usd_value
        usd_total_discount += usd_discount_value
        usd_total_tax += usd_tax_value
        
        eur_total_amount += eur_value
        eur_total_discount += eur_discount_value
        eur_total_tax += eur_tax_value

    grand_total = total_amount + total_tax
    grand_total_USD = usd_total_amount + usd_total_tax
    grand_total_EUR = eur_total_amount + eur_total_tax

    # Create the invoice
    invoice = Invoice(
        order=order,
        billing_address=order.customer.adress,
        total_amount=total_amount,
        total_discount=total_discount,
        tax_amount=total_tax,
        grand_total=grand_total,
        grand_total_USD=grand_total_USD,
        grand_total_EUR=grand_total_EUR
    )
    invoice.save()

    return redirect('order:invoice_detail', invoice_number=invoice.invoice_number)

@login_required
@user_passes_test(is_admin)
def invoice_list(request):
    if request.method == 'POST' and 'delete_invoice' in request.POST:
        invoice_id = request.POST.get('invoice_id')
        invoice = get_object_or_404(Invoice, id=invoice_id)
        order = invoice.order
        invoice.delete()
        order.is_billed = False
        order.save()
        return redirect('order:invoice_list')

    invoices = Invoice.objects.all().order_by('-invoice_date')

    # Removed pagination logic
    return render(request, 'order/invoice_list.html', {'invoices': invoices})

def invoice_detail(request, invoice_number):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    
    if invoice.order.customer.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this info.")
    order = invoice.order
    order_items_with_tl = []

    total_amount = 0
    total_discount = 0
    total_tax = 0
    grand_total = 0
    

    for item in order.order_items.all():
        currency_rate = item.currency_rate
        discount_amount = item.price * item.discount_rate / 100
        tl_value = round((item.price - discount_amount) * currency_rate * item.quantity, 2)
        item_tax = round(tl_value * item.tax / 100, 2)
        item_total = tl_value + item_tax

        total_amount += tl_value
        total_tax += item_tax
        total_discount += round(discount_amount * item.quantity * currency_rate, 2)
        grand_total = total_amount + total_tax

        order_items_with_tl.append({
            'item': item,
            'tl_value': tl_value,
            'currency_rate': currency_rate,
            'tax': item_tax,
            'total': item_total,
            'discount_rate': item.discount_rate
        })

    return render(request, 'order/invoice_detail.html', {
        'invoice': invoice,
        'order': order,
        'total_amount': total_amount,
        'total_tax': total_tax,
        'total_discount': total_discount,
        'order_items_with_tl': order_items_with_tl,
        'grand_total': grand_total,
    })
@login_required
@user_passes_test(is_admin)
def payment_receipt_list(request):
    payment_receipts = PaymentReceipt.objects.all().order_by('-date')

    # Removed pagination logic
    return render(request, 'order/payment_receipt_list.html', {'payment_receipts': payment_receipts})

@login_required
def payment_receipt_detail(request, pk):
    payment_receipt = get_object_or_404(PaymentReceipt, pk=pk)
    if payment_receipt.transaction_type == "Tahsilat":
        if payment_receipt.customer.user != request.user and not request.user.is_superuser:
            return HttpResponseForbidden("You don't have permission to access this info.")
    return render(request, 'order/payment_receipt_detail.html', {'payment_receipt': payment_receipt})

@login_required
@user_passes_test(is_admin)
def payment_receipt_edit(request, pk):
    payment_receipt = get_object_or_404(PaymentReceipt, pk=pk)
    
    if request.method == "POST":
        form = PaymentReceiptForm(request.POST, instance=payment_receipt)
        if form.is_valid():
            form.save()
            return redirect(reverse('order:payment_receipt_detail', args=[payment_receipt.pk]))
    else:
        form = PaymentReceiptForm(instance=payment_receipt)
    
    return render(request, 'order/payment_receipt_edit.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def payment_receipt_create(request):
    if request.method == 'POST':
        form = PaymentReceiptForm(request.POST)
        if form.is_valid():
            payment_receipt = form.save(commit=False)
            payment_receipt.user = request.user
            payment_receipt.save()
            return redirect('order:payment_receipt_detail', pk=payment_receipt.pk)
    else:
        form = PaymentReceiptForm()
    return render(request, 'order/payment_receipt_form.html', {'form': form})
@login_required
@user_passes_test(is_admin)
def customer_search(request):
    query = request.GET.get('q')
    if query:
        customers = Customer.objects.filter(companyName__icontains=query)  # or any field you want to search by
    else:
        customers = Customer.objects.none()
    results = [{'id': customer.id, 'name': customer.companyName} for customer in customers]
    return JsonResponse(results, safe=False)

@login_required
@user_passes_test(is_admin)
def product_order_history(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order_items = OrderItem.objects.filter(product=product, order__is_billed=True).select_related('order__customer').order_by('-order__date')
    
    context = {
        'product': product,
        'order_items': order_items,
    }
    return render(request, 'order/product_order_history.html', context)

@login_required
@user_passes_test(is_admin)
def payment_receipt_delete(request, pk):
    payment_receipt = get_object_or_404(PaymentReceipt, pk=pk)
    if request.method == 'POST':
        payment_receipt.delete()
        return redirect('order:payment_receipt_list')
    return render(request, 'order/payment_receipt_confirm_delete.html', {'payment_receipt': payment_receipt})

@login_required
@user_passes_test(is_admin)
def customer_financials(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    invoices = Invoice.objects.filter(order__customer=customer)
    payments=PaymentReceipt.objects.filter(customer=customer)
    payments_tahsilat = PaymentReceipt.objects.filter(customer=customer, transaction_type=PaymentReceipt.RECEIPT)
    payments_tediye = PaymentReceipt.objects.filter(customer=customer, transaction_type=PaymentReceipt.PAYMENT)
    buyinginvoices=BuyingInvoice.objects.filter(customer=customer)


    # Calculate the total balance
    total_invoiced = sum(invoice.grand_total for invoice in invoices)
    total_payment_tahsilat = sum(payment.amount for payment in payments_tahsilat)
    total_payment_tediye = sum(payment.amount for payment in payments_tediye)
    total_buyinginvoices=sum(buyinginvoice.grand_total_tl for buyinginvoice in buyinginvoices )
    total_balance = total_invoiced - total_buyinginvoices - total_payment_tahsilat + total_payment_tediye

    total_invoiced_usd = sum(invoice.grand_total_USD for invoice in invoices)
    total_payment_tahsilat_usd = sum(payment.usd_amount for payment in payments_tahsilat)
    total_payment_tediye_usd = sum(payment.usd_amount for payment in payments_tediye)
    total_buyinginvoices_usd=sum(buyinginvoice.grand_total_USD for buyinginvoice in buyinginvoices )
    total_balance_usd = total_invoiced_usd - total_buyinginvoices_usd - total_payment_tahsilat_usd + total_payment_tediye_usd

    total_invoiced_eur = sum(invoice.grand_total_EUR for invoice in invoices)
    total_payment_tahsilat_eur = sum(payment.eur_amount for payment in payments_tahsilat)
    total_payment_tediye_eur = sum(payment.eur_amount for payment in payments_tediye)
    total_buyinginvoices_eur=sum(buyinginvoice.grand_total_EUR for buyinginvoice in buyinginvoices )
    total_balance_eur = total_invoiced_eur - total_buyinginvoices_eur - total_payment_tahsilat_eur + total_payment_tediye_eur

    context = {
        'customer': customer,
        'invoices': invoices,
        'payments': payments,
        'buyinginvoices':buyinginvoices,
        'total_balance': total_balance,
        'total_balance_usd':total_balance_usd,
        'total_balance_eur':total_balance_eur
    }
    
    return render(request, 'order/customer_financials.html', context)

@login_required
@user_passes_test(is_admin)
def customer_listed(request):
    search_query = request.GET.get('search', '')
    customers = Customer.objects.all()
    
    if search_query:
        customers = customers.filter(companyName__icontains=search_query)
    
    # Removed pagination logic
    return render(request, 'order/customer_list.html', {'customers': customers})

@login_required
@user_passes_test(is_admin)
def customer_new(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')  # Redirect to customer list page after successful submission
    else:
        form = CustomerForm()

    context = {
        'form': form
    }
    return render(request, 'order/customer_new.html', context)


@login_required
def user_financial(request):
    customer = get_object_or_404(Customer, user=request.user)
    invoices = Invoice.objects.filter(order__customer=customer)
    payments = PaymentReceipt.objects.filter(customer=customer)
    buyinginvoices=BuyingInvoice.objects.filter(customer=customer)

    # Calculate the total balance
    total_invoiced = sum(invoice.grand_total for invoice in invoices)
    total_payments = sum(payment.amount for payment in payments)
    total_buyinginvoices=sum(buyinginvoice.grand_total_tl for buyinginvoice in buyinginvoices )
    total_balance = total_invoiced - total_buyinginvoices - total_payments

    context = {
        'customer': customer,
        'invoices': invoices,
        'payments': payments,
        'buyinginvoices':buyinginvoices,
        'total_balance': total_balance
    }
    
    return render(request, 'order/user_financial.html', context)
@login_required
def user_order(request):
    if "products" not in request.session:
        request.session["products"] = []

    product_form = ProductSearchForm(request.POST)
    productresult = []

    maincategories = mainCategory.objects.all()
    categories = category.objects.all()

    if request.method == "POST":
        if "product_submit" in request.POST:
            if product_form.is_valid():
                query = product_form.cleaned_data["product_name"]
                selected_maincategory = request.POST.get('maincategory')
                selected_category = request.POST.get('category')

                # Split the query into individual words
                query_words = query.split()
                q_objects = Q()
                for word in query_words:
                    q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)

                productresult = Product.objects.filter(q_objects, final_product=True)
                filtered_maincategories = mainCategory.objects.filter(id__in=productresult.values_list('mainCategory_id', flat=True).distinct())
                filtered_categories = category.objects.filter(id__in=productresult.values_list('category_id', flat=True).distinct())

                if selected_maincategory:
                    productresult = productresult.filter(mainCategory_id=selected_maincategory)
                if selected_category:
                    productresult = productresult.filter(category_id=selected_category)
                for product in productresult:
                    product_production = Production.objects.filter(product=product)
                    if product_production:
                        for raw in product_production:
                            product_chip = raw.chip
                            product_empty_cartridge = raw.empty_cartridge

                            # Fetch chip and empty cartridge quantities from inventory
                            stock_chip = Inventory.objects.filter(product=product_chip, place__name="D4").first()
                            stock_empty_cartridge = Inventory.objects.filter(product=product_empty_cartridge, place__name="D4").first()

                            # Ensure the quantities are defaulted to 0 if they don't exist
                            chip_quantity = stock_chip.quantity if stock_chip else 0
                            cartridge_quantity = stock_empty_cartridge.quantity if stock_empty_cartridge else 0

                            # Find the maximum value between chip and cartridge
                            stock_max = max(chip_quantity, cartridge_quantity)

                            # Get the product's inventory quantity
                            inventory = Inventory.objects.filter(product=product, place__name="D1").first()

                            # Ensure inventory quantity is handled properly and sum the max stock with product quantity
                            product_quantity = int(inventory.quantity) if inventory else 0
                            product.stockAmount = product_quantity + int(stock_max)
                    else:
                        # Handle case when no product_production exists
                        inventory = Inventory.objects.filter(product=product, place__name="D1").first()
                        product.stockAmount = int(inventory.quantity) if inventory else 0

                        print("Product Stock Amount:", product.stockAmount)
                productresult = sorted(productresult, key=lambda x: x.stockAmount, reverse=True)

            return render(request, 'order/user_order.html', {
                "product_form": product_form,
                "product": productresult,
                "products": request.session['products'],
                "maincategories": filtered_maincategories,
                "categories": filtered_categories
            })

        elif "product_add" in request.POST:
            product_id = request.POST.get('item_id')
            new_price = float(Product.objects.get(id=product_id).priceSelling)
            quantity = request.POST.get('quantity')
            description = Product.objects.get(id=product_id).description
            currency = Product.objects.get(id=product_id).currency

            if str(currency) == 'USD':
                currency_rate = float(get_currency_rates()[0])
            elif str(currency) == 'EUR':
                currency_rate = float(get_currency_rates()[1])

            product_entry = {
                'id': product_id,
                'price': new_price,
                'quantity': quantity,
                'description': description,
                'currency_rate': currency_rate
            }

            products = request.session.get('products', [])
            products.append(product_entry)
            request.session['products'] = products

        elif "delete_product" in request.POST:
            product_id = request.POST.get('product_id')
            products = request.session.get('products', [])
            products = [product for product in products if product['id'] != product_id]
            request.session['products'] = products

        elif "complete_order" in request.POST:
            customer_id = get_object_or_404(Customer, user=request.user).pk
            product_ids = [item['id'] for item in request.session.get('products', [])]
            quantities = [item['quantity'] for item in request.session.get('products', [])]
            prices = [item['price'] for item in request.session.get('products', [])]
            currencies = [item['currency_rate'] for item in request.session.get('products', [])]

            order = Order.objects.create(customer_id=customer_id, user=request.user)

            for product_id, quantity, price, currency_rate in zip(product_ids, quantities, prices, currencies):
                OrderItem.objects.create(order=order, product_id=product_id, quantity=quantity, price=price, currency_rate=currency_rate, discount_rate=0)

            request.session['products'] = []
            request.session['customers'] = []
            return redirect('order:user_order_list')


        return render(request, 'order/user_order.html', {
            "product_form": product_form,
            "products": request.session['products'],
            "product": productresult,
            "maincategories": maincategories,
            "categories": categories
        })

    else:
        return render(request, 'order/user_order.html', {
            "product_form": product_form,
            "maincategories": maincategories,
            "categories": categories
        })

@login_required
def user_order_list(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        return redirect('order:order_list')

    orders = Order.objects.all().order_by('-date')
    orders_with_totals = []

    for order in orders:
        total_amount_usd = 0
        total_amount_eur = 0
        total_amount_tl = 0
        total_tax = 0
        total_discount=0

        for item in order.order_items.all():
            product = item.product
            if item.discount_rate == 0:
                price_in_tl = item.price * item.quantity * item.currency_rate
                discount=0
            else:
                price_in_tl = item.price *(100-item.discount_rate)/100 * item.quantity * item.currency_rate
                discount=(item.price * item.quantity * item.currency_rate)-(item.price *(100-item.discount_rate)/100 * item.quantity * item.currency_rate)
            product_tax = price_in_tl * product.tax / 100
        
            if str(product.currency) == 'USD':
                total_amount_usd += item.price * item.quantity
            else:  # Assuming it's EUR if not USD
                total_amount_eur += item.price * item.quantity

            total_amount_tl += price_in_tl
            total_tax += product_tax
            total_discount+=discount



        total_amount_tl = round(total_amount_tl, 2)
        total_amount_eur = round(total_amount_eur, 2)
        total_amount_usd=round(total_amount_usd, 2)
        total_discount=round(total_discount, 2)
        total_tax = round(total_tax, 2)
        grand_total = total_amount_tl + total_tax

        orders_with_totals.append({
            'order': order,
            'total_amount_usd': round(total_amount_usd, 2),
            'total_amount_eur': total_amount_eur,
            'total_amount_tl': total_amount_tl,
            'total_discount':total_discount,
            'total_tax': total_tax,
            'grand_total': grand_total,
            'order_date': order.date.strftime('%d-%m-%Y'),  # Adding the order date
        })

    return render(request, 'order/user_order_list.html', {'orders_with_totals': orders_with_totals})

@login_required
def user_invoice_list(request):
    invoices = Invoice.objects.all().order_by('-invoice_date')
    return render(request, 'order/user_invoice_list.html', {'invoices': invoices})

@user_passes_test(lambda u: u.is_superuser)
def post_invoice(request, invoice_number):
    #pip install --upgrade webdriver-manager
    invoices = Invoice.objects.all().order_by('-invoice_date')
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    order = invoice.order

    products = []
    product_price = []
    product_quantity = []

    total_amount = 0
    total_discount = 0
    total_tax = 0
    grand_total = 0

    for item in order.order_items.all():
        currency_rate = item.currency_rate
        discount_amount = item.price * item.discount_rate / 100
        tl_value = round((item.price - discount_amount) * currency_rate * item.quantity, 2)
        item_tax = round(tl_value * item.tax / 100, 2)
        item_total = tl_value + item_tax
        products.append(item.product.description)
        product_price.append((item.price - discount_amount) * currency_rate)
        product_quantity.append(item.quantity)

        total_amount += tl_value
        total_tax += item_tax
        total_discount += round(discount_amount * item.quantity * currency_rate, 2)
        grand_total = total_amount + total_tax

    customer_tax_number = str(order.customer.tax_number)

    # Configure webdriver options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.page_load_strategy = 'normal'
    chrome_options.binary_location = "../usr/local/share/chrome/chrome-linux/chrome"

    service = Service("../usr/local/share/chrome/chrome-linux/chromedriver")  # Point to the correct location of chromedriver
    driver = webdriver.Chrome(service=service,options=chrome_options)#options=chrome_options 

    #driver.maximize_window()
   



    try:
        driver.get('https://portal.smartdonusum.com/accounting/login')

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#username')))

        username_field = driver.find_element(By.CSS_SELECTOR, '#username')
        password_field = driver.find_element(By.CSS_SELECTOR, '#password')

        username_field.send_keys('admin_005256')
        password_field.send_keys('x&2U*bnD')
        password_field.send_keys(Keys.RETURN)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#style-7 > ul > li:nth-child(5) > a'))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#pagesTransformation > ul > li:nth-child(1) > a'))).click()

        input_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#react-select-4--value > div.Select-input > input')))
        input_field.send_keys(customer_tax_number)
        time.sleep(3)
        input_field.send_keys(Keys.TAB)

        try:
            pop_up_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#react > div > div:nth-child(1) > div.wrapper > div.main-panel > div.content > div > div:nth-child(1) > div.sweet-alert > p > span:nth-child(2) > button"))
            )
            pop_up_button.click()
        except (TimeoutException, NoSuchElementException):
            print("No popup appeared")

        for i in range(len(products)):
            item_name_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'#itemName_{i}')))
            item_name_field.send_keys(str(products[i]))
            item_name_field.send_keys(Keys.TAB)
            item_name_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'#quantity_{i}')))
            item_name_field.clear()
            item_name_field.send_keys(str(product_quantity[i]))
            item_name_field.send_keys(Keys.TAB)
            item_name_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'#unitPrice_{i}')))
            item_name_field.clear()
            item_name_field.send_keys(str(product_price[i]).replace('.', ','))
            item_name_field.send_keys(Keys.TAB)
            if i == len(products) - 1:
                break
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#react > div > div:nth-child(1) > div.wrapper > div.main-panel > div.content > div > div.col-sm-12.satirBasi > div.col-sm-12.baseDashboard > div > div.card-header > div > div.col-sm-9 > div > div:nth-child(2) > button'))).click()
            time.sleep(1)
        time.sleep(10)
    finally:
        driver.quit()

    invoice.published = True
    invoice.save()

    return render(request, 'order/invoice_publish_success.html', {'invoices': invoices})
@login_required
def customer_update_request_view(request, pk):
    customer = get_object_or_404(Customer, user_id=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)    
        if form.is_valid():
            updated_data = form.cleaned_data
            update_request = CustomerUpdateRequest(
                customer=customer,
                updated_data=updated_data
            )
            update_request.save()
            return redirect('order/index.html', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'order/customer_update_request.html', {'form': form, 'customer': customer})

@user_passes_test(lambda u: u.is_superuser)
def approve_customer_update_view(request, pk):
    update_request = get_object_or_404(CustomerUpdateRequest, pk=pk)
    if request.method == 'POST':
        if 'approve' in request.POST:
            for field, value in update_request.updated_data.items():
                setattr(update_request.customer, field, value)
            update_request.customer.save()
            update_request.approved = True
            update_request.save()
            return redirect('update_requests_list')
    
    return render(request, 'order/approve_customer_update.html', {'update_request': update_request})

@user_passes_test(lambda u: u.is_superuser)
def invoice_publish(request,invoice_number):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    return render(request, "order/invoice_publish.html",{'invoice':invoice})

@login_required
def make_production(request):
    if "productions" not in request.session:
        request.session["productions"] = []
    if "production_query" not in request.session:
        request.session["production_query"] = ""

    form = ProductSearchForm(request.POST or None)
    productresult = []

    if request.method == "POST":
        if "production_submit" in request.POST:
            if form.is_valid():
                query = form.cleaned_data["product_name"]
                request.session["production_query"] = query
                if query:
                    query_words = query.split()
                    q_objects = Q()
                    for word in query_words:
                        q_objects &= Q(product__description__icontains=word) | Q(product__codeUyum__icontains=word)

                    productresult = Production.objects.filter(q_objects)
                    for production in productresult:
                        inventory = Inventory.objects.filter(product=production.product, place__name="D1").first()
                        production.stockAmount = inventory.quantity if inventory else 0

                    return render(request, "order/production.html", {
                        "form": form,
                        "product": productresult,
                        "productions": request.session["productions"],
                    })

        elif "production_add" in request.POST:
            production_id = request.POST.get("item_id")
            new_powder_gr = request.POST.get("new_powder_gr")
            new_developer_gr = request.POST.get("new_developer_gr")
            quantity = request.POST.get("quantity")
            production = Production.objects.get(id=production_id)
            product_entry = {
                "id": production_id,
                "new_powder_gr": new_powder_gr,
                "new_developer_gr": new_developer_gr,
                "quantity": quantity,
                "description": production.product.description,
            }

            productions = request.session.get("productions", [])
            productions.append(product_entry)
            request.session["productions"] = productions

            query = request.session.get("production_query", "")
            if query:
                query_words = query.split()
                q_objects = Q()
                for word in query_words:
                    q_objects &= Q(product__description__icontains=word) | Q(product__codeUyum__icontains=word)

                productresult = Production.objects.filter(q_objects)
                for production in productresult:
                    inventory = Inventory.objects.filter(product=production.product, place__name="D1").first()
                    production.stockAmount = inventory.quantity if inventory else 0

            return render(request, "order/production.html", {
                "form": form,
                "product": productresult,
                "productions": request.session["productions"],
            })

        elif "delete_production" in request.POST:
            production_id = request.POST.get("production_id")
            productions = request.session.get("productions", [])
            productions = [production for production in productions if production["id"] != production_id]
            request.session["productions"] = productions

            query = request.session.get("production_query", "")
            if query:
                query_words = query.split()
                q_objects = Q()
                for word in query_words:
                    q_objects &= Q(product__description__icontains=word) | Q(product__codeUyum__icontains=word)

                productresult = Production.objects.filter(q_objects)
                for production in productresult:
                    inventory = Inventory.objects.filter(product=production.product, place__name="D1").first()
                    production.stockAmount = inventory.quantity if inventory else 0

            return render(request, "order/production.html", {
                "form": form,
                "product": productresult,
                "productions": request.session["productions"],
            })

        elif "complete_production" in request.POST:
            production_ids = [item["id"] for item in request.session.get("productions", [])]
            quantities = [item["quantity"] for item in request.session.get("productions", [])]
            new_powder_grs = [item["new_powder_gr"] for item in request.session.get("productions", [])]
            new_developer_grs = [item["new_developer_gr"] for item in request.session.get("productions", [])]

            for production_id, quantity, new_powder_gr, new_developer_gr in zip(production_ids, quantities, new_powder_grs, new_developer_grs):
                production = Production.objects.get(id=production_id)
                # Save the production process or perform necessary updates here

            request.session["productions"] = []
            request.session["production_query"] = ""

            return redirect("order:make_production")

    return render(request, "order/production.html", {
        "form": form,
        "product": productresult,
        "productions": request.session["productions"],
    })

@login_required
def change_product (request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductSearchForm()
    if form.is_valid():
        query = form.cleaned_data["product_name"]
    if query:
        productresult = Production.objects.filter(product__description__icontains=query)
        return render(request, "order/change_product.html", {"form": form, "product": productresult})
    else:
        return render(request, "order/production.html", {"form": form, "product": productresult})

@login_required
@user_passes_test(is_admin)
def supplier_new(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order:supplier_listed')  # Redirect to customer list page after successful submission
    else:
        form = SupplierForm()

    context = {
        'form': form
    }
    return render(request, 'order/supplier_new.html', context)


@login_required
@user_passes_test(is_admin)
def supplier_listed(request):
    suppliers = Supplier.objects.all()

    search_query = request.GET.get('search')
    if search_query:
        suppliers = suppliers.filter(companyName__icontains=search_query)

    # Removed pagination logic
    return render(request, 'order/supplier_list.html', {'suppliers': suppliers})


@login_required
@user_passes_test(is_admin)
def supplier_list(request):
    if "suppliers" not in request.session:
        request.session["suppliers"] = []
    if "products" not in request.session:
        request.session["products"] = []
    if "product_query" not in request.session:
        request.session["product_query"] = ""

    supplier_list = []
    supplier_selected = request.session['suppliers']
    product_form = ProductSearchForm(request.POST or None)
    productresult = []  # Initialize productresult
    places = Place.objects.all()  # Fetch all places here

    if request.method == "POST" and "supplier_searched" in request.POST:
        input_supplier = request.POST.get('supplier')
        supplier_list = Supplier.objects.filter(companyName__icontains=input_supplier)
        if not supplier_list:
            messages.info(request, 'No suppliers found matching your search.')
        return render(request, 'order/purchase_create.html', {
            "supplier_list": supplier_list,
            "supplier_selected": supplier_selected,
            "places": places,  # Pass places to the template
        })

    elif request.method == "POST" and "supplier_selected" in request.POST:
        request.session['suppliers'] = []
        supplier_id = request.POST.get('supplier_id')
        supplier_name = Supplier.objects.get(id=supplier_id).companyName
        request.session['suppliers'].append(supplier_id)
        return render(request, 'order/purchase_create.html', {
            "supplier_name": supplier_name,
            "product_form": product_form,
            "products": request.session['products'],
            "places": places,  # Pass places to the template
        })

    elif request.method == "POST" and "product_submit" in request.POST:
        supplier_name = Supplier.objects.get(id=request.session['suppliers'][0]).companyName
        if product_form.is_valid():
            query = product_form.cleaned_data["product_name"]
            request.session['product_query'] = query  # Store the search query in the session
            if query:
                # Split the query into individual words
                query_words = query.split()
                # Create a Q object to combine conditions
                q_objects = Q()
                for word in query_words:
                    # Update the Q object with each word
                    q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)
                
                # Filter products based on the Q object
                productresult = Product.objects.filter(q_objects)
                return render(request, 'order/purchase_create.html', {
                    "product_form": product_form,
                    "product": productresult,
                    "supplier_name": supplier_name,
                    "products": request.session['products'],
                    "places": places,  # Pass places to the template
                })

    elif request.method == "POST" and "product_add" in request.POST:
        product_id = request.POST.get('item_id')
        new_price = request.POST.get('new_price')
        quantity = request.POST.get('quantity')
        place_id = request.POST.get('place_id')
        place_name = Place.objects.get(id=place_id).name  # Get the place name
        description = Product.objects.get(id=product_id).description
        currency=Product.objects.get(id=product_id).currency.currency
        tax=Product.objects.get(id=product_id).tax
        #tax = request.POST.get(f'tax_{item.id}')

        product_entry = {
            'id': product_id,
            'price': new_price,
            'quantity': quantity,
            'description': description,
            'place_id': place_id,
            'place_name': place_name,  # Include place name
            'currency': currency,
            'tax': tax
        }

        products = request.session.get('products', [])
        products.append(product_entry)
        request.session['products'] = products

        supplier_name = Supplier.objects.get(id=request.session['suppliers'][0]).companyName

        query = request.session.get('product_query', "")
        if query:
            # Split the query into individual words
            query_words = query.split()
            # Create a Q object to combine conditions
            q_objects = Q()
            for word in query_words:
                # Update the Q object with each word
                q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)

            # Filter products based on the Q object
            productresult = Product.objects.filter(q_objects)

            # Retrieve stock amount from Inventory where place is "D1"
            for product in productresult:
                inventory = Inventory.objects.filter(product=product, place__name="D1").first()
                product.stockAmount = inventory.quantity if inventory else 0

        return render(request, 'order/purchase_create.html', {
            "product_form": product_form,
            "supplier_name": supplier_name,
            "products": request.session['products'],
            "product": productresult,
            "places": places,
            
        })

    elif request.method == "POST" and "delete_product" in request.POST:
        product_id = request.POST.get('product_id')
        products = request.session.get('products', [])
        products = [product for product in products if product['id'] != product_id]
        request.session['products'] = products

        supplier_name = Supplier.objects.get(id=request.session['suppliers'][0]).companyName

        query = request.session.get('product_query', "")
        if query:
            # Split the query into individual words
            query_words = query.split()
            # Create a Q object to combine conditions 
            q_objects = Q()
            for word in query_words:
                # Update the Q object with each word
                q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)
            
            # Filter products based on the Q object
            productresult = Product.objects.filter(q_objects)

            # Retrieve stock amount from Inventory where place is "D1"
            for product in productresult:
                inventory = Inventory.objects.filter(product=product, place__name="D1").first()
                product.stockAmount = inventory.quantity if inventory else 0

        
        return render(request, 'order/purchase_create.html', {
            "product_form": product_form,
            "supplier_name": supplier_name,
            "products": request.session['products'],
            "product": productresult,
            "places": places,  # Pass places to the template
        })
    elif request.method == "POST" and "complete_purchase" in request.POST:
        supplier_id = request.session['suppliers'][0]
        supplier = Supplier.objects.get(id=supplier_id)
        
        # Retrieve products from session
        products = request.session.get('products', [])
        
        # Create a new buying invoice
        buying_invoice = BuyingInvoice.objects.create(
            supplier=supplier,
            billing_address=supplier.adress,
            total_amount_tl=0,  # This will be calculated later
            total_discount=0,  # If applicable
            tax_amount=0,  # If applicable
            grand_total_tl=0,  # This will be calculated later
        )

        total_amount_USD = 0
        total_amount_EUR = 0
        total_amount_tl = 0
        total_tax = 0
        total_discount = 0
  
        # Create buying items and update inventory
        for product_entry in products:
            product = Product.objects.get(id=product_entry['id'])
            place = Place.objects.get(id=product_entry['place_id'])
            quantity = int(product_entry['quantity'])
            price = float(product_entry['price'])
            tax = Product.objects.get(id=product_entry['id']).tax
            
            if str(product_entry["currency"]) == 'USD':
                currency_rate = float(get_currency_rates()[0])
                total_amount_USD += price * quantity
                total_amount_tl += price * quantity * currency_rate
 
            if str(product_entry["currency"]) == 'EUR':
                currency_rate = float(get_currency_rates()[1])
                total_amount_EUR += price * quantity
                total_amount_tl += price * quantity * currency_rate

            # Update Inventory
            inventory, created = Inventory.objects.get_or_create(product=product, place=place, defaults={'quantity': 0})
            inventory.update_quantity(quantity, increase=True)  # Increase the inventory
            inventory.priceBuying = price
            inventory.save()

            # Create BuyingItem
            BuyingItem.objects.create(
                buying_invoice=buying_invoice,
                product=product,
                inventory=inventory,
                quantity=quantity,
                price=price,
                currency_rate=currency_rate,  # Assuming default rate, update if necessary
                discount_rate=0  # Assuming no discount, update if necessary
            )
        
        # Update buying invoice totals
        buying_invoice.total_amount_tl = total_amount_tl
        buying_invoice.total_amount_USD = total_amount_USD
        buying_invoice.total_amount_EUR = total_amount_EUR

        # Calculate tax, discounts and grand total if applicable
        buying_invoice.save()

        # Clear session data
        request.session['suppliers'] = []
        request.session['products'] = []
        request.session['product_query'] = ""

        messages.success(request, "Purchase completed successfully!")

        return render(request, 'order/purchase_create.html', {
            "product_form": product_form,
            "supplier_selected": [],
            "products": [],
            "places": places,  # Pass places to the template
        })
    
    else:
        return render(request, 'order/purchase_create.html', {
            "product_form": product_form,
            "supplier_selected": supplier_selected,
            "places": places,  # Pass places to the template
        })

@login_required
@user_passes_test(is_admin)
def buying_invoice_list(request):
    if request.method == 'POST' and 'delete_invoice' in request.POST:
        invoice_id = request.POST.get('invoice_id')
        invoice = get_object_or_404(BuyingInvoice, id=invoice_id)
        
        # Update inventory quantities before deleting the invoice
        for item in invoice.buying_items.all():
            inventory = item.inventory
            inventory.quantity -= item.quantity
            inventory.save()

        invoice.delete()
        return redirect('order:buying_invoice_list')

    invoices = BuyingInvoice.objects.all().order_by('-invoice_date')
    
    # Removed pagination logic
    return render(request, 'order/buying_invoice_list.html', {'invoices': invoices})

@login_required
def buying_invoice_detail(request, invoice_number):
    invoice = get_object_or_404(BuyingInvoice, invoice_number=invoice_number)
    defaultUSD, defaultEUR = get_currency_rates()  # Assuming you have this function available
    product_form = ProductSearchForm(request.POST or None)
    places = Place.objects.all()

    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this info.")

    invoice_items = []
    total_amount_tl = 0
    total_amount_USD = 0
    total_amount_EUR = 0

    total_discount = 0
    total_tax = 0
    grand_total = 0

    for item in invoice.buying_items.all():
        currency_rate = item.currency_rate
        discount_amount = item.price * item.discount_rate / 100
        tl_value = round((item.price - discount_amount) * currency_rate * item.quantity, 2)
        item_tax = round(tl_value * item.tax / 100, 2)
        item_total = tl_value + item_tax
        total_amount_tl += tl_value
        total_tax += item_tax
        total_discount += round(discount_amount * item.quantity * currency_rate, 2)
        grand_total = total_amount_tl + total_tax

        if str(item.product.currency) == "USD":
            total_amount_USD =round((item.price - discount_amount) * item.quantity, 2)

        if str(item.product.currency) == "EUR":
            total_amount_EUR = round((item.price - discount_amount) * item.quantity, 2)

        invoice_items.append({
            'item': item,
            'tl_value': tl_value,
            'currency_rate': currency_rate,
            'tax': item_tax,
            'total': item_total,
            'discount_rate': item.discount_rate,
            'total_amount_USD': total_amount_USD,
            'total_amount_EUR': total_amount_EUR,
        })

    productresult = None

    if request.method == 'POST':
        if 'product_submit' in request.POST:
            if product_form.is_valid():
                query = product_form.cleaned_data.get("product_name", "")
                if query:
                    query_words = query.split()
                    q_objects = Q()
                    for word in query_words:
                        q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)
                    productresult = Product.objects.filter(q_objects)

                    for product in productresult:
                        inventory = Inventory.objects.filter(product=product, place__name="D1").first()
                        product.stockAmount = inventory.quantity if inventory else 0

                    for product in productresult:
                        product.stockAmount = f"{product.stockAmount:,.2f}"
                else:
                    productresult = []
        elif 'delete_item' in request.POST:
            item_id = request.POST.get('delete_item')
            item = get_object_or_404(BuyingItem, id=item_id, buying_invoice=invoice)
            item.delete()
            return redirect('order:buying_invoice_detail', invoice_number=invoice.invoice_number)
        
        elif 'product_add' in request.POST:
            product_id = request.POST.get('item_id')
            new_price = request.POST.get('new_price')
            quantity = request.POST.get('quantity')
            place_id = request.POST.get('place_id')
            product = get_object_or_404(Product, id=product_id)
            currency = product.currency
            place = get_object_or_404(Place, id=place_id)

            if str(currency) == 'USD':
                currency_rate = float(defaultUSD)
            elif str(currency) == 'EUR':
                currency_rate = float(defaultEUR)
            else:
                currency_rate = 1
            
            inventory, created = Inventory.objects.get_or_create(product=product, place=place)
            inventory.priceBuying = new_price
            inventory.quantity += int(quantity)  # Update inventory quantity
            inventory.save()

            buying_item = BuyingItem(
                buying_invoice=invoice,
                product=product,
                inventory=inventory,
                quantity=int(quantity),
                price=float(new_price),
                currency_rate=currency_rate,
                discount_rate=0
            )
            buying_item.save()
            return redirect('order:buying_invoice_detail', invoice_number=invoice.invoice_number)

        else:
            for item in invoice.buying_items.all():
                if f'update_item_{item.id}' in request.POST:
                    old_quantity = item.quantity
                    new_quantity = int(request.POST.get(f'quantity_{item.id}', item.quantity))
                    item.quantity = new_quantity
                    item.price = request.POST.get(f'price_{item.id}', item.price)
                    item.currency_rate = request.POST.get(f'currency_rate_{item.id}', item.currency_rate)
                    item.discount_rate = request.POST.get(f'discount_rate_{item.id}', item.discount_rate)
                    item.tax = request.POST.get(f'tax_rate_{item.id}', item.tax)  # Update tax rate
                    item.save()

                    # Update inventory quantity based on the difference between old and new quantity
                    inventory = item.inventory
                    inventory.quantity += (new_quantity - old_quantity)
                    inventory.save()

            return redirect('order:buying_invoice_detail', invoice_number=invoice.invoice_number)

    return render(request, 'order/buying_invoice_detail.html', {
        'invoice': invoice,
        'invoice_items': invoice_items,
        'total_amount_tl': total_amount_tl,
        'total_tax': total_tax,
        'total_discount': total_discount,
        'grand_total': grand_total,
        'product_form': product_form,
        'productresult': productresult,
        'places': places
    })
@login_required
@user_passes_test(is_admin)
def supplier_financials(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    buying_invoices = BuyingInvoice.objects.filter(supplier=supplier)
    payments = PaymentReceipt.objects.filter(supplier=supplier)

    # Calculate the total balance
    total_invoiced_USD = sum(buying_invoice.grand_total_USD for buying_invoice in buying_invoices)
    total_invoiced_EUR = sum(buying_invoice.grand_total_EUR for buying_invoice in buying_invoices)
    total_invoiced_tl = sum(buying_invoice.grand_total_tl for buying_invoice in buying_invoices)

  
    total_payments_USD = sum(payment.usd_amount for payment in payments)
    total_payments_EUR = sum(payment.eur_amount for payment in payments)
    total_payments_tl = sum(payment.amount for payment in payments)
    
    
    total_balance_USD = total_invoiced_USD - total_payments_USD
    total_balance_EUR=total_invoiced_EUR-total_payments_EUR
    total_balance_tl=total_invoiced_tl-total_payments_tl


    context = {
        'supplier': supplier,
        'buying_invoices': buying_invoices,
        'payments': payments,
        'total_balance_USD': total_balance_USD,
        'total_balance_EUR': total_balance_EUR,
        'total_balance_tl': total_balance_tl,
        

        
    }
    
    return render(request, 'order/supplier_financials.html', context)

@login_required
@user_passes_test(is_admin)
def loc_supplier_list(request):
    if "suppliers" not in request.session:
        request.session["suppliers"] = []
    if "products" not in request.session:
        request.session["products"] = []
    if "product_query" not in request.session:
        request.session["product_query"] = ""

    supplier_list = []
    supplier_selected = request.session['suppliers']
    product_form = ProductSearchForm(request.POST or None)
    productresult = []  # Initialize productresult
    places = Place.objects.all()  # Fetch all places here

    if request.method == "POST" and "supplier_searched" in request.POST:
        input_supplier = request.POST.get('supplier')
        supplier_list = Customer.objects.filter(companyName__icontains=input_supplier)
        if not supplier_list:
            messages.info(request, 'No suppliers found matching your search.')
        return render(request, 'order/purchase_create_loc.html', {
            "supplier_list": supplier_list,
            "supplier_selected": supplier_selected,
            "places": places,  # Pass places to the template
        })

    elif request.method == "POST" and "supplier_selected" in request.POST:
        request.session['suppliers'] = []
        supplier_id = request.POST.get('supplier_id')
        supplier_name = Customer.objects.get(id=supplier_id).companyName
        request.session['suppliers'].append(supplier_id)
        return render(request, 'order/purchase_create_loc.html', {
            "supplier_name": supplier_name,
            "product_form": product_form,
            "products": request.session['products'],
            "places": places,  # Pass places to the template
        })

    elif request.method == "POST" and "product_submit" in request.POST:
        supplier_name = Customer.objects.get(id=request.session['suppliers'][0]).companyName
        if product_form.is_valid():
            query = product_form.cleaned_data["product_name"]
            request.session['product_query'] = query  # Store the search query in the session
            if query:
                # Split the query into individual words
                query_words = query.split()
                # Create a Q object to combine conditions
                q_objects = Q()
                for word in query_words:
                    # Update the Q object with each word
                    q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)
                
                # Filter products based on the Q object
                productresult = Product.objects.filter(q_objects)
                return render(request, 'order/purchase_create_loc.html', {
                    "product_form": product_form,
                    "product": productresult,
                    "supplier_name": supplier_name,
                    "products": request.session['products'],
                    "places": places,  # Pass places to the template
                })

    elif request.method == "POST" and "product_add" in request.POST:
        product_id = request.POST.get('item_id')
        new_price = request.POST.get('new_price')
        quantity = request.POST.get('quantity')
        place_id = request.POST.get('place_id')
        place_name = Place.objects.get(id=place_id).name  # Get the place name
        description = Product.objects.get(id=product_id).description
        currency=Product.objects.get(id=product_id).currency.currency
        tax=Product.objects.get(id=product_id).tax

        product_entry = {
            'id': product_id,
            'price': new_price,
            'quantity': quantity,
            'description': description,
            'place_id': place_id,
            'place_name': place_name,  # Include place name
            'currency': currency,
            'tax': tax
        }

        products = request.session.get('products', [])
        products.append(product_entry)
        request.session['products'] = products

        supplier_name = Customer.objects.get(id=request.session['suppliers'][0]).companyName

        query = request.session.get('product_query', "")
        if query:
            # Split the query into individual words
            query_words = query.split()
            # Create a Q object to combine conditions
            q_objects = Q()
            for word in query_words:
                # Update the Q object with each word
                q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)

            # Filter products based on the Q object
            productresult = Product.objects.filter(q_objects)

            # Retrieve stock amount from Inventory where place is "D1"
            for product in productresult:
                inventory = Inventory.objects.filter(product=product, place__name="D1").first()
                product.stockAmount = inventory.quantity if inventory else 0

        return render(request, 'order/purchase_create_loc.html', {
            "product_form": product_form,
            "supplier_name": supplier_name,
            "products": request.session['products'],
            "product": productresult,
            "places": places,
            
        })

    elif request.method == "POST" and "delete_product" in request.POST:
        product_id = request.POST.get('product_id')
        products = request.session.get('products', [])
        products = [product for product in products if product['id'] != product_id]
        request.session['products'] = products

        supplier_name = Customer.objects.get(id=request.session['suppliers'][0]).companyName

        query = request.session.get('product_query', "")
        if query:
            # Split the query into individual words
            query_words = query.split()
            # Create a Q object to combine conditions 
            q_objects = Q()
            for word in query_words:
                # Update the Q object with each word
                q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)
            
            # Filter products based on the Q object
            productresult = Product.objects.filter(q_objects)

            # Retrieve stock amount from Inventory where place is "D1"
            for product in productresult:
                inventory = Inventory.objects.filter(product=product, place__name="D1").first()
                product.stockAmount = inventory.quantity if inventory else 0

        
        return render(request, 'order/purchase_create_loc.html', {
            "product_form": product_form,
            "supplier_name": supplier_name,
            "products": request.session['products'],
            "product": productresult,
            "places": places,  # Pass places to the template
        })
    elif request.method == "POST" and "complete_purchase" in request.POST:
        supplier_id = request.session['suppliers'][0]
        supplier = Customer.objects.get(id=supplier_id)
        
        # Retrieve products from session
        products = request.session.get('products', [])
        
        # Create a new buying invoice
        buying_invoice = BuyingInvoice.objects.create(
            customer=supplier,
            billing_address=supplier.adress,
            total_amount_tl=0,  # This will be calculated later
            total_discount=0,  # If applicable
            tax_amount=0,  # If applicable
            grand_total_tl=0,  # This will be calculated later
        )

        total_amount_USD = 0
        total_amount_EUR = 0
        total_amount_tl = 0
        total_tax = 0
        total_discount = 0
  
        # Create buying items and update inventory
        for product_entry in products:
            product = Product.objects.get(id=product_entry['id'])
            place = Place.objects.get(id=product_entry['place_id'])
            quantity = int(product_entry['quantity'])
            price = float(product_entry['price'])
            tax = Product.objects.get(id=product_entry['id']).tax
            
            if str(product_entry["currency"]) == 'USD':
                currency_rate = float(get_currency_rates()[0])
                total_amount_USD += price * quantity
                total_amount_tl += price * quantity * currency_rate
 
            if str(product_entry["currency"]) == 'EUR':
                currency_rate = float(get_currency_rates()[1])
                total_amount_EUR += price * quantity
                total_amount_tl += price * quantity * currency_rate

            # Update Inventory
            inventory, created = Inventory.objects.get_or_create(product=product, place=place, defaults={'quantity': 0})
            inventory.update_quantity(quantity, increase=True)  # Increase the inventory
            inventory.priceBuying = price
            inventory.save()

            # Create BuyingItem
            BuyingItem.objects.create(
                buying_invoice=buying_invoice,
                product=product,
                inventory=inventory,
                quantity=quantity,
                price=price,
                currency_rate=currency_rate,  # Assuming default rate, update if necessary
                discount_rate=0  # Assuming no discount, update if necessary
            )
        
        # Update buying invoice totals
        buying_invoice.total_amount_tl = total_amount_tl
        buying_invoice.total_amount_USD = total_amount_USD
        buying_invoice.total_amount_EUR = total_amount_EUR

        # Calculate tax, discounts and grand total if applicable
        buying_invoice.save()

        # Clear session data
        request.session['suppliers'] = []
        request.session['products'] = []
        request.session['product_query'] = ""

        messages.success(request, "Purchase completed successfully!")

        return render(request, 'order/purchase_create_loc.html', {
            "product_form": product_form,
            "supplier_selected": [],
            "products": [],
            "places": places,  # Pass places to the template
        })
    
    else:
        return render(request, 'order/purchase_create_loc.html', {
            "product_form": product_form,
            "supplier_selected": supplier_selected,
            "places": places,  # Pass places to the template
        })


@login_required
@user_passes_test(is_admin)
def accounts_listed(request):
    bankaccounts = CashRegister.objects.all()
    
    # Removed pagination logic
    return render(request, 'order/accounts_list.html', {'bankaccounts': bankaccounts})


@login_required
@user_passes_test(is_admin)
def account_detail_list(request, id):
    account = get_object_or_404(CashRegister, id=id)
    transactions = Transaction.objects.filter(cash_register=account)
    currency_account = account.currency

    return render(request, 'order/account_detail_list.html', {'transactions': transactions, 'currency_account': currency_account})
@login_required
def transfer_money(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            source_register = form.cleaned_data['source_register']
            target_register = form.cleaned_data['target_register']
            amount = form.cleaned_data['amount']
            fee = form.cleaned_data['fee']
            expense_item = form.cleaned_data['expense_item']
            
            if source_register.transfer(amount, target_register, fee, expense_item, request.user):
                messages.success(request, 'Money transferred successfully.')
                return redirect('order:accounts_list')
            else:
                form.add_error(None, 'Insufficient funds in the source register.')
    else:
        form = TransferForm()
    
    return render(request, 'order/transfer_money.html', {'form': form})

def customer_signup(request):
    if request.method == 'POST':
        user_form = CustomerSignUpForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False  # Deactivate account until it is confirmed
            user.save()

            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('order/signup_succes.html')
    else:
        user_form = CustomerSignUpForm()
        customer_form = CustomerForm()
    return render(request, 'order/customer_signup.html', {
        'user_form': user_form,
        'customer_form': customer_form
    })

def signup_success(request):
    return render(request, 'order/signup_succes.html')