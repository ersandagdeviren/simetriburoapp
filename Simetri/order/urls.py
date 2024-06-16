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
    path('create_invoice/<str:order_number>/', views.create_invoice, name='create_invoice'),
]