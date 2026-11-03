from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
from .form import CustomUserForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    products = Product.objects.filter(trending = 1, status = 0)
    return render(request, 'shop/index.html', {"products": products})

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration success !!!")
            print("Registration success !!!")
            return redirect('login')
    return render(request, 'shop/register.html', {"form": form})

def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    else: 
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=user, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!!!")
                return redirect("home")
        return render(request, 'shop/login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout success")
    return redirect("home")

def collections(request):
    category = Category.objects.filter(status=1)
    return render(request, "shop/collections.html", {"Category": category})

def collectionView(request, product):
    if Category.objects.filter(name = product, status=1):
        products = Product.objects.filter(category__name = product, status=0)
        return render(request, "shop/products/index.html", {"products": products, "category_name": product })
    else:
        messages.warning(request, "No such category found")
        print(request.build_absolute_uri())
        return redirect('collections') 

def productDetails(request, cname, pname):
    if Category.objects.filter(name=cname, status=1):
        if Product.objects.filter(name=pname, status=0):
            products = Product.objects.filter(name=pname, status=0).first()
            return render(request, "shop/products/product_details.html", {"products": products})
        else:
            messages.error(request, "No such product found")
            print(request.build_absolute_uri())
            return redirect('collections')
    else:
        messages.error(request, "No such category found")
        print(request.build_absolute_uri())
        return redirect('collections')

def cart(request):
    pass