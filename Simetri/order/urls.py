from django.urls import path
from . import views

app_name="order"
urlpatterns = [
    path("", views.main, name="main"),
    path("search/",views.search, name ="search"),
    path("comparison", views.comparison, name="comparison"),
    path("create/",views.customer_list, name="customer_list"),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<str:order_number>/', views.order_detail, name='order_detail'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoice/<str:invoice_number>/', views.invoice_detail, name='invoice_detail'),
    path('order/<str:order_number>/create_invoice/', views.create_invoice, name='create_invoice'),
    path('payment_receipts/', views.payment_receipt_list, name='payment_receipt_list'),
    path('payment_receipts/<int:pk>/', views.payment_receipt_detail, name='payment_receipt_detail'),
    path('payment_receipts/new/', views.payment_receipt_create, name='payment_receipt_create'),
    path('payment_receipt/<int:pk>/delete/', views.payment_receipt_delete, name='payment_receipt_delete'),
    path('customer_search/', views.customer_search, name='customer_search'),
    path('product/<int:product_id>/order-history/', views.product_order_history, name='product_order_history'),
]
