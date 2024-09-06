from django.urls import path
from Simetri.users import views
app_name="users"
urlpatterns=[
    path("",views.index, name="index"),
    path("login",views.login_view, name="login"),
    path("logout",views.logout_view, name="logout")
]