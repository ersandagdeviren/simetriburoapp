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
    path('invoice_post/<str:invoice_number>/', views.post_invoice, name='post_invoice'),
    path('invoice_publish/<str:invoice_number>/', views.invoice_publish, name='invoice_publish'),
    path('order/<str:order_number>/create_invoice/', views.create_invoice, name='create_invoice'),
    path('payment_receipts/', views.payment_receipt_list, name='payment_receipt_list'),
    path('payment_receipts/<int:pk>/', views.payment_receipt_detail, name='payment_receipt_detail'),
    path('payment_receipt/<int:pk>/edit/', views.payment_receipt_edit, name='payment_receipt_edit'),
    path('payment_receipts/new/', views.payment_receipt_create, name='payment_receipt_create'),
    path('payment_receipt/<int:pk>/delete/', views.payment_receipt_delete, name='payment_receipt_delete'),
    path('customer_search/', views.customer_search, name='customer_search'),
    path('customers/', views.customer_listed, name='customer_listed'),
    path('product/<int:product_id>/order-history/', views.product_order_history, name='product_order_history'),
    path('customer_new/', views.customer_new, name="customer_new"),
    path('customer/<int:customer_id>/financials/', views.customer_financials, name='customer_financials'),
    path('customer/user_financial/', views.user_financial, name='user_financial'),
    path('customer/user_order/', views.user_order, name='user_order'),
    path('customer/user_order_list/', views.user_order_list, name='user_order_list'),
    path('customer/user_invoice_list/', views.user_invoice_list, name='user_invoice_list'),
    path('customer/<int:pk>/update/', views.customer_update_request_view, name='customer_update_request'),
    path('customer/update/<int:pk>/approve/', views.approve_customer_update_view, name='approve_customer_update'),
    path('customer/<int:id>/', views.customer_details, name='customer_details'),
  
]
