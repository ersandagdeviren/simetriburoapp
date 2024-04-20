from django.shortcuts import render,get_object_or_404,redirect
from django import forms
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import urllib.request
from django.contrib.auth.decorators import login_required
from .models import product, customer
from .forms import *
from django.contrib import messages

@login_required
def search(request):
    if request.method=="POST":
        form=ProductSearchForm( request.POST)
        if form.is_valid():
            query=form.cleaned_data["product_name"]
            productresult=[]
            if query:
                productresult=product.objects.filter(description__icontains=query)
                return render(request,"order/product.html",{"form":form,"product":productresult})
            else:
                return render(request, "order/product.html",{"form":ProductSearchForm()})
    else:
        return render(request, "order/product.html",{"form":ProductSearchForm()})

@login_required
def main(request):
    webpage_response = requests.get('https://canlidoviz.com/doviz-kurlari/garanti-bankasi')
    webpage = webpage_response.content
    soup = BeautifulSoup(webpage, "html.parser")
    target_data_usd = soup.select_one("html > body > div:nth-of-type(3) > div > div:nth-of-type(3) > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(4) > table > tbody > tr:nth-of-type(1) > td:nth-of-type(3) > div > span").get_text()
    target_data_usd=round(float(str(target_data_usd).replace(" ","").replace("\n","")),2)
    target_data_eur=soup.select_one("html > body > div:nth-of-type(3) > div > div:nth-of-type(3) > div > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(4) > table > tbody > tr:nth-of-type(2) > td:nth-of-type(3) > div > span").get_text()
    target_data_eur=round(float(str(target_data_eur).replace(" ","").replace("\n","")),2)

    webpage_response2=requests.get('https://www.altinkaynak.com/Doviz/Kur/Guncel')
    webpage2=webpage_response2.content
    soup2=BeautifulSoup(webpage2, "html.parser")
    target_data_usd2=round(float(soup2.find( id="tdUSDSell").get_text().replace(",",".")),2)
    target_data_eur2=round(float(soup2.find( id="tdEURSell").get_text().replace(",",".")),2)

    return render(request, "order/base.html",{"target_data_usd":target_data_usd,"target_data_eur":target_data_eur,"target_data_usd2":target_data_usd2,"target_data_eur2":target_data_eur2})

@login_required
def comparison(request):
    return render(request, "order/comparison.html")

@login_required
def customer_list(request):

    if "customner" not in request.session:
        request.session["customer"]=[]
        
    customer_list = []
    customer_selected=request.session['customers']
    product_form=ProductSearchForm(request.POST)

    if request.method == "POST" and "customer_searched" in request.POST:
        input_customer = request.POST.get('customer')
        customer_list = customer.objects.filter(companyName__icontains=input_customer)
        if not customer_list:
            messages.info(request, 'Aramanızla eşleşen müşteri bulunamadı.')
        return render(request, 'order/order_create.html', {
            "customer_list": customer_list,
            "customer_selected":customer_selected,
            })

    elif request.method == "POST" and "customer_selected" in request.POST:
        request.session['customers'] = []
        customer_id = request.POST.get('customer_id')
        customer_name=(customer.objects.get(id=customer_id)).companyName
        request.session['customers'].append(customer_id)
        print(request.session['customers'])
        return render(request, 'order/order_create.html', {
            "customer_name":customer_name,
            "product_form":product_form
            })
    
    elif request.method == "POST" and "product_submit" in request.POST:
        productresult=[]
        customer_name=customer.objects.get(id=request.session['customers'][0]).companyName
        if product_form.is_valid():
            query=product_form.cleaned_data["product_name"]
            if query:
                productresult=product.objects.filter(description__icontains=query)
                return render(request,'order/order_create.html',{
                    "product_form":product_form,
                    "product":productresult,
                    "customer_name":customer_name,
                    })
            else:
                return render(request, 'order/order_create.html',{"form":ProductSearchForm()})
            

    return render(request, 'order/order_create.html', {
        "customer_list": customer_list,
        "customer_selected":customer_selected,
        })
