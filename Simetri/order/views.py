from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django import forms
from django.utils import timezone
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from order.models import Product, Customer, Order, OrderItem, Invoice,CashRegister,ExpenseItem,PaymentReceipt, CustomerUpdateRequest
from .forms import ProductSearchForm ,PaymentReceiptForm,CustomerForm, CustomerUpdateRequestForm
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
    if request.method == "POST":
        form = ProductSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["product_name"]
            productresult = []

            if query:
                # Split the query into individual words
                query_words = query.split()
                # Create a Q object to combine conditions
                q_objects = Q()
                for word in query_words:
                    # Update the Q object with each word
                    q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)
                
                # Filter products based on the Q object
                productresult = Product.objects.filter(q_objects).order_by('-stockAmount')

                # Format numerical values with thousand separators
                for product in productresult:
                    product.stockAmount = f"{product.stockAmount:,.2f}"

                return render(request, "order/product.html", {"form": form, "product": productresult})
            else:
                return render(request, "order/product.html", {"form": ProductSearchForm()})
    else:
        return render(request, "order/product.html", {"form": ProductSearchForm()})

@login_required
def main(request):
    webpage_response = requests.get('https://canlidoviz.com/doviz-kurlari/garanti-bankasi')
    webpage = webpage_response.content
    soup = BeautifulSoup(webpage, "html.parser")
    target_data_usd = soup.select_one(
        "body > div.flex.w-full.justify-center.px-3 > div > div.flex.flex-col.sc1300\:flex-row.justify-center.max-w-\[1500px\].gap-3.min-w-0 > div > div.flex.gap-3.w-full.flex-col.lg\:flex-row > div.w-full > div.flex.lg\:px-3.flex-col.flex-\[1_1_auto\].lg\:bg-pholder.lg\:theme-dark\:bg-dPholder.lg\:theme-light\:bg-wPholder.shadow-boxShadow > div.py-0 > table > tbody > tr:nth-child(1) > td.align-middle.md\:align-top.text-right.w-24.truncate.ml-6 > div").get_text()
    print("------------------aaa--------------------------------------")
    print(target_data_usd)
    target_data_usd = round(float(str(target_data_usd).replace(" ", "").replace("\n", "")[:5]), 2)
    target_data_usd = round(target_data_usd, 2)  # Keep it as a float for now

    target_data_eur = soup.select_one(
        "body > div.flex.w-full.justify-center.px-3 > div > div.flex.flex-col.sc1300\:flex-row.justify-center.max-w-\[1500px\].gap-3.min-w-0 > div > div.flex.gap-3.w-full.flex-col.lg\:flex-row > div.w-full > div.flex.lg\:px-3.flex-col.flex-\[1_1_auto\].lg\:bg-pholder.lg\:theme-dark\:bg-dPholder.lg\:theme-light\:bg-wPholder.shadow-boxShadow > div.py-0 > table > tbody > tr:nth-child(2) > td.align-middle.md\:align-top.text-right.w-24.truncate.ml-6 > div").get_text()
    target_data_eur = round(float(str(target_data_eur).replace(" ", "").replace("\n", "")[:5]), 2)
    target_data_eur = round(target_data_eur, 2)  # Keep it as a float for now

    webpage_response2 = requests.get('https://www.altinkaynak.com/Doviz/Kur/Guncel')
    webpage2 = webpage_response2.content
    soup2 = BeautifulSoup(webpage2, "html.parser")
    target_data_usd2 = round(float(soup2.find(id="tdUSDSell").get_text().replace(",", ".")), 2)
    target_data_usd2 = round(target_data_usd2, 2)  # Keep it as a float for now

    target_data_eur2 = round(float(soup2.find(id="tdEURSell").get_text().replace(",", ".")), 2)
    target_data_eur2 = round(target_data_eur2, 2)  # Keep it as a float for now

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
                productresult = Product.objects.filter(q_objects).order_by('-stockAmount')
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
            productresult = Product.objects.filter(q_objects).order_by('-stockAmount')

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
            productresult = Product.objects.filter(q_objects).order_by('-stockAmount')

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

        return render(request, 'order/order_create.html', {
            "product_form": product_form,
        })
    else:
        return render(request, 'order/order_create.html', {
            "product_form": product_form,
            "customer_selected": customer_selected,
        })


@login_required
def create_order(request):
    if request.method == "POST" and "create_order" in request.POST:
        customer_id = request.session.get('customers', [None])[0]
        product_ids = request.session.get('products', [])
        if not customer_id or not product_ids:
            messages.error(request, 'Customer and products must be selected to create an order.')
            return redirect('order:create_order')

        order = Order(customer_id=customer_id, user=request.user)
        order.save()
        
        for product_id in product_ids:
            product = Product.objects.get(id=product_id)
            quantity = int(request.POST.get(f'quantity_{product_id}', 1))
            order_item = OrderItem(order=order, product=product, quantity=quantity, price=product.priceSelling)
            order_item.save()

        request.session['customers'] = []
        request.session['products'] = []
        return redirect('order:order_list')
    else:
        product_form = ProductSearchForm()
        customer_selected = request.session.get('customers', [])
        customer_name = None
        if customer_selected:
            customer_name = Customer.objects.get(id=customer_selected[0]).companyName
        

        return render(request, 'order/order_create.html', {
            "product_form": product_form,
            "customer_name": customer_name,
            "products": request.session.get('products', [])
        })
    
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
                    productresult = Product.objects.filter(q_objects).order_by('-stockAmount')
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

        else:
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
    
    # Check stock for each item in the order
    for item in order.order_items.all():
        if item.product.stockAmount < item.quantity:
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
            usd_tax_value = round(usd_value * item.product.tax / 100, 2)
        else:
            usd_value = 0
            usd_discount_value = 0
            usd_tax_value = 0

        if str(item.product.currency) == 'EUR':
            eur_value = round((item.price - (item.price * item.discount_rate / 100)) * item.quantity, 2)
            eur_discount_value = (item.price * item.discount_rate / 100)
            eur_tax_value = round(eur_value * item.product.tax / 100, 2)
        else:
            eur_value = 0
            eur_discount_value = 0
            eur_tax_value = 0

        tl_value = round((item.price - (item.price * item.discount_rate / 100)) * item.currency_rate * item.quantity, 2)
        discount_value_tl = (item.price * item.discount_rate / 100) * item.currency_rate
        tax_value_tl = round(tl_value * item.product.tax / 100, 2)

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
    payment_receipts = PaymentReceipt.objects.all()
    return render(request, 'order/payment_receipt_list.html', {'payment_receipts': payment_receipts})

@login_required
def payment_receipt_detail(request, pk):
    payment_receipt = get_object_or_404(PaymentReceipt, pk=pk)
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
    payments = PaymentReceipt.objects.filter(customer=customer)

    # Calculate the total balance
    total_invoiced = sum(invoice.grand_total for invoice in invoices)
    total_payments = sum(payment.amount for payment in payments)
    total_balance = total_invoiced - total_payments

    context = {
        'customer': customer,
        'invoices': invoices,
        'payments': payments,
        'total_balance': total_balance
    }
    
    return render(request, 'order/customer_financials.html', context)

@login_required
@user_passes_test(is_admin)
def customer_listed(request):
    customers = Customer.objects.all()

    # Handle search functionality
    search_query = request.GET.get('search')
    if search_query:
        customers = customers.filter(companyName__icontains=search_query)

    context = {
        'customers': customers
    }
    return render(request, 'order/customer_list.html', context)
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

    # Calculate the total balance
    total_invoiced = sum(invoice.grand_total for invoice in invoices)
    total_payments = sum(payment.amount for payment in payments)
    total_balance = total_invoiced - total_payments

    context = {
        'customer': customer,
        'invoices': invoices,
        'payments': payments,
        'total_balance': total_balance
    }
    
    return render(request, 'order/user_financial.html', context)
@login_required
def user_order (request):
    if "products" not in request.session:
        request.session["products"] = []

    product_form = ProductSearchForm(request.POST)
    productresult = []  # Initialize productresult



    if request.method == "POST" and "product_submit" in request.POST:
        if product_form.is_valid():
            query = product_form.cleaned_data["product_name"]
            if query:
                # Split the query into individual words
                query_words = query.split()
                # Create a Q object to combine conditions
                q_objects = Q()
                for word in query_words:
                    # Update the Q object with each word
                    q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)
                
                # Filter products based on the Q object
                productresult = Product.objects.filter(q_objects).order_by('-stockAmount')
                return render(request, 'order/user_order.html', {
                    "product_form": product_form,
                    "product": productresult,
                    "products": request.session['products']
                })

    elif request.method == "POST" and "product_add" in request.POST:
        product_id = request.POST.get('item_id')
        new_price = float(Product.objects.get(id=product_id).priceSelling)
        quantity = request.POST.get('quantity')
        description = Product.objects.get(id=product_id).description
        currency=Product.objects.get(id=product_id).currency
       
        if str(currency)== 'USD':
            currency_rate=float(get_currency_rates()[0])
        if str(currency)== 'EUR':
            currency_rate=float(get_currency_rates()[1])

        

        product_entry = {
            'id': product_id,
            'price': new_price,
            'quantity': quantity,
            'description': description,
            'currency_rate':currency_rate
        }

        products = request.session.get('products', [])
        products.append(product_entry)
        request.session['products'] = products


        if product_form.is_valid():
            query = product_form.cleaned_data["product_name"]
            productresult = []

            if query:
                # Split the query into individual words
                query_words = query.split()
                # Create a Q object to combine conditions
                q_objects = Q()
                for word in query_words:
                    # Update the Q object with each word
                    q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)
                
                # Filter products based on the Q object
                productresult = Product.objects.filter(q_objects).order_by('-stockAmount')

        return render(request, 'order/user_order.html', {
            "product_form": product_form,
            "products": request.session['products'],
            "product": productresult
        })

    elif request.method == "POST" and "delete_product" in request.POST:
        product_id = request.POST.get('product_id')
        products = request.session.get('products', [])
        products = [product for product in products if product['id'] != product_id]
        request.session['products'] = products

        if product_form.is_valid():
            query = product_form.cleaned_data["product_name"]
            productresult = []

            if query:
                # Split the query into individual words
                query_words = query.split()
                # Create a Q object to combine conditions
                q_objects = Q()
                for word in query_words:
                    # Update the Q object with each word
                    q_objects &= Q(description__icontains=word) | Q(codeUyum__icontains=word)
                
                # Filter products based on the Q object
                productresult = Product.objects.filter(q_objects).order_by('-stockAmount')

        return render(request, 'order/user_order.html', {
            "product_form": product_form,
            "products": request.session['products'],
            "product": productresult
        })
    elif request.method == "POST" and "complete_order" in request.POST:
        customer_id = get_object_or_404(Customer,user=request.user).pk
        product_ids = [item['id'] for item in request.session.get('products', [])]
        quantities = [item['quantity'] for item in request.session.get('products', [])]
        prices = [item['price'] for item in request.session.get('products', [])]
        currencies=[item['currency_rate'] for item in request.session.get('products', [])]

        order = Order.objects.create(customer_id=customer_id,user=request.user)

        for product_id, quantity, price, currency_rate in zip(product_ids, quantities, prices,currencies):
            OrderItem.objects.create(order=order, product_id=product_id, quantity=quantity, price=price,currency_rate=currency_rate,discount_rate=0)

        request.session['products'] = []
        request.session['customers'] = []


        return render(request, 'order/user_order.html', {
            "product_form": product_form,
        })
    else:
        return render(request, 'order/user_order.html', {
            "product_form": product_form,
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
def post_invoice(request,invoice_number):
    invoices = Invoice.objects.all().order_by('-invoice_date')
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    order = invoice.order
    order_items_with_tl = []

    total_amount = 0
    total_discount = 0
    total_tax = 0
    grand_total = 0
    
    products=[]
    product_price=[]
    product_quantity=[]

    for item in order.order_items.all():
        currency_rate = item.currency_rate
        discount_amount = item.price * item.discount_rate / 100
        tl_value = round((item.price - discount_amount) * currency_rate * item.quantity, 2)
        item_tax = round(tl_value * item.product.tax / 100, 2)
        item_total = tl_value + item_tax
        products.append(item.product.description)
        product_price.append((item.price - discount_amount) * currency_rate)
        product_quantity.append(item.quantity)



        total_amount += tl_value
        total_tax += item_tax
        total_discount += round(discount_amount * item.quantity * currency_rate, 2)
        grand_total = total_amount + total_tax
        item_quantity=item.quantity
        customer_tax_number=str(item.order.customer.tax_number)


    # Configure webdriver options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up the webdriver using webdriver_manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), ) #options=chrome_options
    driver.maximize_window()
    try:
        # Open the login page
        driver.get('https://portal.smartdonusum.com/accounting/login')
        
        # Wait until the username field is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#username')))

        # Locate the username and password fields
        username_field = driver.find_element(By.CSS_SELECTOR, '#username')
        password_field = driver.find_element(By.CSS_SELECTOR, '#password')

        # Enter the username and password
        username_field.send_keys('admin_005256')
        password_field.send_keys('x&2U*bnD')
        # Submit the form
        password_field.send_keys(Keys.RETURN)


        # Click on the specified elements
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#style-7 > ul > li:nth-child(5) > a'))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#pagesTransformation > ul > li:nth-child(1) > a'))).click()

        # Wait for the input field to be visible and send the number
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
        pass
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

