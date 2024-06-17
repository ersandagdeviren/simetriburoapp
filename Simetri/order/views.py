from django.shortcuts import render, redirect,get_object_or_404
from django import forms
from django.utils import timezone
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from .models import Product, Customer, Order, OrderItem, Invoice
from .forms import ProductSearchForm
from decimal import Decimal, ROUND_HALF_UP

def currency():
    webpage_response = requests.get('https://canlidoviz.com/doviz-kurlari/garanti-bankasi')
    webpage = webpage_response.content
    soup = BeautifulSoup(webpage, "html.parser")
    target_data_usd = soup.select_one("html > body > div:nth-of-type(3) > div > div:nth-of-type(3) > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(4) > table > tbody > tr:nth-of-type(1) > td:nth-of-type(3) > div > span").get_text()
    target_data_usd = Decimal(str(target_data_usd).replace(" ", "").replace("\n", "")).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    target_data_eur = soup.select_one("html > body > div:nth-of-type(3) > div > div:nth-of-type(3) > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(4) > table > tbody > tr:nth-of-type(2) > td:nth-of-type(3) > div > span").get_text()
    target_data_eur = Decimal(str(target_data_eur).replace(" ", "").replace("\n", "")).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    return target_data_usd, target_data_eur

defaultUSD, defaultEUR = currency()

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
def search(request):
    if request.method == "POST":
        form = ProductSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["product_name"]
            productresult = []

            if query:
                productresult = Product.objects.filter(description__icontains=query)
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
        "html > body > div:nth-of-type(3) > div > div:nth-of-type(3) > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(4) > table > tbody > tr:nth-of-type(1) > td:nth-of-type(3) > div > span").get_text()
    target_data_usd = round(float(str(target_data_usd).replace(" ", "").replace("\n", "")), 2)
    target_data_eur = soup.select_one(
        "html > body > div:nth-of-type(3) > div > div:nth-of-type(3) > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(4) > table > tbody > tr:nth-of-type(2) > td:nth-of-type(3) > div > span").get_text()
    target_data_eur = round(float(str(target_data_eur).replace(" ", "").replace("\n", "")), 2)

    webpage_response2 = requests.get('https://www.altinkaynak.com/Doviz/Kur/Guncel')
    webpage2 = webpage_response2.content
    soup2 = BeautifulSoup(webpage2, "html.parser")
    target_data_usd2 = round(float(soup2.find(id="tdUSDSell").get_text().replace(",", ".")), 2)
    target_data_eur2 = round(float(soup2.find(id="tdEURSell").get_text().replace(",", ".")), 2)

    return render(request, "order/base.html", {
        "target_data_usd": target_data_usd, 
        "target_data_eur": target_data_eur,
        "target_data_usd2": target_data_usd2, 
        "target_data_eur2": target_data_eur2
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

    customer_list = []
    customer_selected = request.session['customers']
    product_form = ProductSearchForm(request.POST)
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
            if query:
                productresult = Product.objects.filter(description__icontains=query)
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
        currency=Product.objects.get(id=product_id).currency

        if str(currency)== 'USD':
            currency_rate=float(defaultUSD)
        if str(currency)== 'EUR':
            currency_rate=float(defaultEUR)

        

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

        customer_name = Customer.objects.get(id=request.session['customers'][0]).companyName

        if product_form.is_valid():
            query = product_form.cleaned_data["product_name"]
            productresult = Product.objects.filter(description__icontains=query)

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

        if product_form.is_valid():
            query = product_form.cleaned_data["product_name"]
            productresult = Product.objects.filter(description__icontains=query)

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
        currencies=[item['currency_rate'] for item in request.session.get('products', [])]

        order = Order.objects.create(customer_id=customer_id,user=request.user)

        for product_id, quantity, price, currency_rate in zip(product_ids, quantities, prices,currencies):
            OrderItem.objects.create(order=order, product_id=product_id, quantity=quantity, price=price,currency_rate=currency_rate,discount_rate=0)

        request.session['products'] = []
        request.session['customers'] = []

        messages.success(request, 'Order completed successfully.')

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

        order = Order(customer_id=customer_id, user=request.user)  # Add user here
        order.save()

        for product_id in product_ids:
            product = Product.objects.get(id=product_id)
            quantity = int(request.POST.get(f'quantity_{product_id}', 1))
            order_item = OrderItem(order=order, product=product, quantity=quantity, price=product.priceSelling)
            order_item.save()

        messages.success(request, 'Order created successfully.')
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
def order_list(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        messages.success(request, 'Order has been successfully deleted.')
        return redirect('order:order_list')

    orders = Order.objects.all()
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

    return render(request, 'order/order_list.html', {'orders_with_totals': orders_with_totals})


def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    product_form = ProductSearchForm(request.POST or None)
    productresult = None 

    if request.method == 'POST':
        if 'product_submit' in request.POST:
            if product_form.is_valid():
                query = product_form.cleaned_data.get("product_name", "")
                if query:
                    productresult = Product.objects.filter(description__icontains=query)
                else:
                    productresult = []
        elif 'delete_item' in request.POST:
            item_id = request.POST.get('delete_item')
            item = get_object_or_404(OrderItem, id=item_id, order=order)
            item.delete()
            messages.success(request, 'Order item has been successfully deleted.')
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
            messages.success(request, 'Product has been successfully added to the order.')
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
            messages.success(request, 'Order items have been successfully updated.')
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
def create_invoice(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    
    # Check if an invoice already exists for the order
    if hasattr(order, 'invoice'):
        messages.error(request, 'Invoice already exists for this order.')
        return redirect('order:order_detail', order_number=order_number)
    
    total_amount = 0
    total_discount = 0
    total_tax = 0
    grand_total = 0
    total_amount_USD_tax=0
    total_amount_EUR_tax=0
    grand_total_EUR=0
    grand_total_USD=0


    for item in order.order_items.all():
        currency_rate = item.currency_rate
        discount_amount = item.price * item.discount_rate / 100
        tl_value = round((item.price - discount_amount) * currency_rate * item.quantity, 2)
        currency_value_tax = round((item.price - discount_amount) * item.quantity * (Decimal('1.00') + item.product.tax / Decimal('100.00')), 2)
        if str(item.product.tax) == 'USD':
            total_amount_USD_tax +=currency_value_tax
        if str(item.product.tax) == 'EUR':
            total_amount_EUR_tax+=currency_value_tax
        
        item_tax = round(tl_value * item.product.tax / 100, 2)
        item_total = tl_value + item_tax




        total_amount += tl_value
        total_tax += item_tax
        total_discount += round(discount_amount * item.quantity * currency_rate, 2)
        grand_total = total_amount + total_tax
        grand_total_EUR=round(grand_total/ Decimal(float(defaultEUR)),2)
        grand_total_USD=round(grand_total/ Decimal(float(defaultUSD)),2)
        


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

    messages.success(request, 'Invoice has been successfully created.')
    return redirect('order:invoice_detail', invoice_number=invoice.invoice_number)

def invoice_list(request):
    if request.method == 'POST' and 'delete_invoice' in request.POST:
        invoice_id = request.POST.get('invoice_id')
        invoice = get_object_or_404(Invoice, id=invoice_id)
        order = invoice.order
        invoice.delete()
        order.is_billed = False
        order.save()
        messages.success(request, 'Invoice has been successfully deleted.')
        return redirect('order:invoice_list')

    invoices = Invoice.objects.all()
    invoices_with_details = []

    for invoice in invoices:
        order = invoice.order
        total_amount_usd = Decimal('0.00')
        total_amount_USD_tax = Decimal('0.00')
        total_amount_eur = Decimal('0.00')
        total_amount_EUR_tax = Decimal('0.00')
        total_amount_tl = Decimal('0.00')
        total_tax = Decimal('0.00')
        total_discount = Decimal('0.00')

        for item in order.order_items.all():
            product = item.product
            currency_rate = Decimal(item.currency_rate)
            if item.discount_rate == 0:
                price_in_tl = item.price * item.quantity * currency_rate
                discount = Decimal('0.00')
            else:
                price_in_tl = item.price * (Decimal('100.00') - item.discount_rate) / Decimal('100.00') * item.quantity * currency_rate
                discount = (item.price * item.quantity * currency_rate) - (item.price * (Decimal('100.00') - item.discount_rate) / Decimal('100.00') * item.quantity * currency_rate)
            product_tax = price_in_tl * product.tax / Decimal('100.00')
            
            if str(product.currency) == 'USD':
                total_amount_usd += item.price * item.quantity
                total_amount_USD_tax += item.price * item.quantity * (Decimal('1.00') + item.product.tax / Decimal('100.00'))
            elif str(product.currency) == 'EUR':
                total_amount_eur += item.price * item.quantity
                total_amount_EUR_tax += item.price * item.quantity * (Decimal('1.00') + item.product.tax / Decimal('100.00'))
            else:
                total_amount_tl += item.price * item.quantity * currency_rate
            
            total_amount_tl += price_in_tl
            total_tax += product_tax
            total_discount += discount

        total_amount_tl = round(total_amount_tl, 2)
        total_amount_eur = round(total_amount_eur, 2)
        total_amount_EUR_tax = round(total_amount_EUR_tax, 2)
        total_amount_usd = round(total_amount_usd, 2)
        total_amount_USD_tax = round(total_amount_USD_tax, 2)
        total_discount = round(total_discount, 2)
        total_tax = round(total_tax, 2)
        grand_total = total_amount_tl + total_tax
        grand_total_EUR = round(grand_total / Decimal(float(defaultEUR)), 2)
        grand_total_USD = round(grand_total / Decimal(float(defaultUSD)), 2)

        invoices_with_details.append({
            'invoice': invoice,
            'order': order,
            'total_amount_usd': total_amount_usd,
            'total_amount_eur': total_amount_eur,
            'total_amount_EUR_tax': grand_total_EUR,
            'total_amount_USD_tax': grand_total_USD,
            'total_amount_tl': total_amount_tl,
            'total_discount': total_discount,
            'total_tax': total_tax,
            'grand_total': grand_total,
            'invoice_date': invoice.invoice_date.strftime('%d-%m-%Y'),  # Adding the invoice date
        })

    return render(request, 'order/invoice_list.html', {'invoices_with_details': invoices_with_details})
def invoice_detail(request, invoice_number):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
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
