from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
from .form import CustomUserForm
from django.contrib.auth import authenticate, login, logout
import json
from django.http import JsonResponse

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
            user = authenticate(request, username=name, password=pwd)
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

def addToCart(request):
    if request.method == 'POST':
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            if request.user.is_authenticated:
                data = json.load(request)
                print(data['product_qty'])
                print(data['pid'])
                product_status = Product.objects.get(id=data['pid'])
                if product_status:
                    if Cart.objects.filter(user=request.user, product_id = data['pid']):
                        return JsonResponse({'Status' : 'Product already in Cart'},safe=False ,status=200)
                    elif product_status.quantity >= data['product_qty']:
                        Cart.objects.create(user=request.user, product_id = data['pid'], product_qty = data['product_qty'])
                        return JsonResponse({'Status' : 'Product added to Cart'},safe=False ,status=200)
                    else:
                        return JsonResponse({'Status' : 'Product Out of Stock'},safe=False ,status=200)
            else:
                return JsonResponse({'Login to Account'}, status=200)
        else:
            return JsonResponse({'Invalid Access'}, status=200)

def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user = request.user)
        return render(request, "shop/cart.html", {"cart": cart})
    else:
        return redirect('home')

def removeCart(request, cid):
    cartItems = Cart.objects.get(id=cid)
    cartItems.delete()
    return redirect('cart')

def fav(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id = data['pid']
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user, product_id=product_id):
                    return JsonResponse({'status': 'Product already in Favourites'}, status=200)
                else:
                    Favourite.objects.create(user=request.user, product_id = product_id)
                    return JsonResponse({'status': 'Product added to Favourites'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add Favourites'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid access'}, status=200)

def favViewPage(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user=request.user)
        return render(request, 'shop/fav.html', {"fav": fav})
    else:
        return redirect("home")

def favRemove(request, pid):
    favItems = Favourite.objects.get(id=pid)
    favItems.delete()
    return redirect('favviewpage')