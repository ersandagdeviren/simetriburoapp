from django.shortcuts import render, redirect,get_object_or_404
from django import forms
from django.utils import timezone
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from .models import Product, Customer, Order, OrderItem
from .forms import ProductSearchForm

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

        product_entry = {
            'id': product_id,
            'price': new_price,
            'quantity': quantity,
            'description': description
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

        order = Order.objects.create(customer_id=customer_id)

        for product_id, quantity, price in zip(product_ids, quantities, prices):
            OrderItem.objects.create(order=order, product_id=product_id, quantity=quantity, price=price)

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

        order = Order(customer_id=customer_id)
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
        total_amount = sum(item.price * item.quantity for item in order.order_items.all())
        orders_with_totals.append({
            'order': order,
            'total_amount': total_amount
        })
    
    return render(request, 'order/order_list.html', {'orders_with_totals': orders_with_totals})

def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    if request.method == 'POST':
        if 'delete_item' in request.POST:
            item_id = request.POST.get('delete_item')
            item = get_object_or_404(OrderItem, id=item_id, order=order)
            item.delete()
            messages.success(request, 'Order item has been successfully deleted.')
            return redirect('order:order_detail', order_number=order.order_number)
        
        for item in order.order_items.all():
            quantity = request.POST.get(f'quantity_{item.id}')
            price = request.POST.get(f'price_{item.id}')
            if quantity is not None and price is not None:
                item.quantity = int(quantity)
                item.price = float(price)
                item.save()
        messages.success(request, 'Order items have been successfully updated.')
        return redirect('order:order_detail', order_number=order.order_number)
    
    total_amount = sum(item.price * item.quantity for item in order.order_items.all())
    return render(request, 'order/order_detail.html', {'order': order, 'total_amount': total_amount})