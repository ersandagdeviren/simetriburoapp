from django.urls import path
from . import views

app_name="order"
urlpatterns = [
    path("", views.main, name="main"),
    path("search/",views.search, name ="search"),
    path("comparison", views.comparison, name="comparison"),
    path("create/",views.customer_list, name="customer_list"),
]