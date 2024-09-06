from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.cache import never_cache
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render (request,"users/user.html")
    
@never_cache
def login_view(request):
    if request.method == "POST":
        username= request.POST["username"]
        password= request.POST["password"]
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("Simetri.order:main"))
        else:
            return render (request, "users/login.html",{
                "message": "Invalid Credentials"
            })
    return render(request, "users/login.html")

def logout_view(request):

    logout(request)
    return render(request, "users/login.html",{
        "message":"Logged Out"
    })